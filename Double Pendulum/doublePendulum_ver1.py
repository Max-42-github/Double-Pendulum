import numpy as np
from scipy.integrate  import odeint
import matplotlib.pyplot as plt

g = 9.8

m1 = 2
m2 = 1
l1 = 2
l2 = 1

def doublePendulum(X,t):
	t1, omega1, t2, omega2 = X


	'''

	t1Dot = omega1
	t2Dot = omega2

	term3a = ((2*np.sin(t1-t2))*(m2*(((omega1**2)*(l2))*((omega1**2)*(l2)*(np.cos(t1-t2))))))/(l1*((2*m1)+(m2)+(m2*(np.cos((2*t1)-t2)))))

	t1DDot = (-g*((2*m1) + m2)*(np.sin(t1))) - ((m2*g)*(np.sin(t1-(2*t2)))) - (term3a)

	t2DDot = ((2*np.sin(t1-t2))*(((omega1**2)*l1*(m1+m2))+(g*(m1+m2)*(np.cos(t1)))+((omega2**2)*l2*m2*(np.cos(t1-t2)))))/(l2*((2*m1)+(m2)-(m2*np.cos((2*t1)-(2*t2))))) 

	'''


	t1Dot = omega1
	t2Dot = omega2

	deno1 = ((m1+m2)*(l1)) - (m1*l1*(np.cos(t2-t1)**2))

	t1DDot = ((m2*l1*(t1Dot**2)*(np.sin(t2-t1))*(np.cos(t2-t1)))+(m2*g*(np.sin(t2))*(np.cos(t2-t1)))+(m2*l2*(t2Dot**2)*(np.sin(t2-t1)))-((m1+m2)*g*(np.sin(t1))))/(deno1)

	deno2 = ((m1+m2)*(l2)) - (m2*l2*(np.cos(t2-t1)**2))

	t2DDot = ((m2*l2*(t2Dot**2)*(np.sin(t2-t1))*(np.cos(t2-t1)))+((m1+m2)*((g*(np.sin(t1))*(np.cos(t2-t1)))-(l1*(t2Dot**2)*(np.sin(t2-t1)))-(g*(np.sin(t2))))))/(deno2)

	return [t1Dot, t1DDot, t2Dot, t2DDot]



# Initial Cond.
X0 = [1,-3,-1,5]

# time array
tArr = np.linspace(0,10,1000)


solution = odeint(doublePendulum,X0,tArr)

print(type(solution))
print(np.shape(solution))


y1 = solution[:,0]
y2 = solution[:,2]

pos1x = l1*(np.sin(y1))
pos1y = -l1*(np.cos(y1))

pos2x = pos1x + l2*(np.sin(y2))
pos2y = pos1y - l2*(np.cos(y2))


print(np.shape(y1))
print(np.shape(y2))


plt.figure(figsize = (7,7))

plt.xlim(-4,4)
plt.ylim(-4,4)

plt.grid()

plt.title('Double Pendulum')
plt.xlabel('x ->')
plt.ylabel('y ->')

#plt.plot(pos1x,pos1y)
plt.plot(pos2x,pos2y)

plt.show()


