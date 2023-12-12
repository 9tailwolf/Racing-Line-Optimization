import math
from tqdm import tqdm
import time
from classes.Vector import Vector

class Optimizer:
    def __init__(self,rx,ry,lx,ly,norm,node_size:int,max_velocity:int,min_velocity:int,velocity_interval:int,max_theta:int,theta_interval:int):
        '''
        Tuned value for limit physical movements.
        It is recommended to use the above values s fixed values.
        Surely, there is a better tuned value. But it is hard to find.
        '''
        self.centripetal_force_limiter = 3000
        self.degree_limiter = 10
        self.accelation_degree_limiter = 3

        rx_temp = rx.copy()
        ry_temp = ry.copy()
        lx_temp = lx.copy()
        ly_temp = ly.copy()

        self.data = {'rx':rx_temp, 'ry':ry_temp, 'lx':lx_temp, 'ly':ly_temp}
        self.length = len(rx)

        self.norm = norm
        self.node_size = node_size
        self.max_velocity = max_velocity
        self.min_velocity = min_velocity
        self.velocity_interval = velocity_interval
        self.max_theta = max_theta
        self.theta_interval = theta_interval # odd

        for k in self.data.keys():
            self.data[k].append(self.data[k][-1])

    def get_velocity(self,i):
        if i<0 or i>= self.velocity_interval:
            raise 'Velocity Error'

        return (i) * (self.max_velocity-self.min_velocity) / (self.velocity_interval-1) + self.min_velocity

    def get_theta(self,i):
        if i<0 or i>= self.theta_interval:
            raise 'Theta Error'

        return (i * (self.max_theta * 2 / self.theta_interval - 1) - self.max_theta) / 180 * math.pi


    def memoization(self):
        if self.node_size<3:
            raise 'Size Error'

        dp = [[[[math.inf for _ in range(self.theta_interval)] for _ in range(self.velocity_interval)] for _ in range(self.node_size)] for _ in range(self.length)]

        dp_posx, dp_posy = [], []
        for i in range(self.length+1):
            x = [-1 for _ in range(self.node_size)]
            y = [-1 for _ in range(self.node_size)]
            x[0],x[-1],y[0],y[-1] = self.data['rx'][i],self.data['lx'][i],self.data['ry'][i],self.data['ly'][i]

            gap_x = (self.data['rx'][i] - self.data['lx'][i]) / (self.node_size - 1)
            gap_y = (self.data['ry'][i] - self.data['ly'][i]) / (self.node_size - 1)

            for i in range(1,self.node_size-1):
                x[i] = x[i-1] - gap_x
                y[i] = y[i-1] - gap_y

            dp_posx.append(x)
            dp_posy.append(y)

        self.dp_posx = dp_posx
        self.dp_posy = dp_posy


        return dp

    def optimization(self):
        dp = self.memoization()
        selected = [[[[-1 for _ in range(self.theta_interval)] for _ in range(self.velocity_interval)] for _ in range(self.node_size)] for _ in range(self.length)]

        for node in range(self.node_size):
            for v in range(self.velocity_interval):
                for t in range(self.theta_interval):
                    dp[0][node][v][t] = 0

        for i in tqdm(range(1,self.length)):
            time.sleep(10**-6)
            for node in range(self.node_size): # current position
                for v in range(self.velocity_interval): # current speed
                    for t in range(self.theta_interval): # current angle
                        for pre_node in range(self.node_size): # previous position
                            for pre_v in range(self.velocity_interval): # previous speed
                                for pre_t in range(self.theta_interval): # previous angle
                                    if dp[i-1][pre_node][pre_v][pre_t] == math.inf:
                                        pass

                                    if dp[i][node][v][t] > dp[i-1][pre_node][pre_v][pre_t] + self.cost(i,node,v,t,i-1,pre_node,pre_v,pre_t):
                                        selected[i][node][v][t] = (pre_node,pre_v,pre_t)
                                        dp[i][node][v][t] = dp[i-1][pre_node][pre_v][pre_t] + self.cost(i,node,v,t,i-1,pre_node,pre_v,pre_t)


        res = math.inf
        result_pos = []
        result_vector = None

        for node in range(self.node_size):
            for v in range(self.velocity_interval):
                for t in range(self.theta_interval):
                    if res > dp[-1][node][v][t]:
                        res = dp[-1][node][v][t]
                        result_vector = selected[i][node][v][t]

        result_pos.append(result_vector[0])

        for i in range(self.length - 2,0,-1):
            result_vector = selected[i][result_vector[0]][result_vector[1]][result_vector[2]]
            result_pos.append(result_vector[0])

        result_pos.reverse()
        result_posx, result_posy = [],[]
        for i in range(len(result_pos)):
            result_posx.append(self.dp_posx[i][result_pos[i]])
            result_posy.append(self.dp_posy[i][result_pos[i]])
        return result_posx, result_posy


    def cost(self, i1, node1, v1, t1, i2, node2, v2, t2):
        '''
        acceleration penelty
        '''
        if abs(v1 - v2)>1:
            return math.inf

        '''
        delta time
        '''
        v1vector = self.norm[i1].rotate(self.get_theta(t1)) * self.get_velocity(v1)
        v2vector = self.norm[i2].rotate(self.get_theta(t2)) * self.get_velocity(v2)
        avgv = (v1vector + v2vector) / 2
        ds = Vector(self.dp_posx[i1][node1] - self.dp_posx[i2][node2], self.dp_posy[i1][node1] - self.dp_posy[i2][node2])
        dt = ds.size() / avgv.size()
        if min(ds.degree(avgv) / math.pi * 180, 180 - ds.degree(avgv)/ math.pi * 180) > self.degree_limiter:
            return math.inf


        '''
        centripetal force penalty
        '''
        r = ds.size() / (v1vector.degree(v2vector) / math.pi * 180 + 10**-6)
        centripetal_accelation = avgv.size()**2 / r
        if centripetal_accelation > self.centripetal_force_limiter:
            return math.inf

        '''
        accelation penalty
        '''
        accelation = abs(v1vector.size() ** 2 - v2vector.size() ** 2) / (2 * ds.size())
        if accelation > 0 and min(ds.degree(avgv) / math.pi * 180, 180 - ds.degree(avgv)/ math.pi * 180) > self.accelation_degree_limiter:
            return math.inf

        return dt