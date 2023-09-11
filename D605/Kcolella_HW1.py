#%%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
#%%

#%%
x = np.concatenate([
    np.repeat(0,100),
    np.linspace(0,0.5,100),
    np.linspace(0,0.5,100),
    np.repeat(1,50),
    np.linspace(1,1.15,25),
    np.linspace(1,1.15,25),
    np.linspace(1.15,1.4,25),
    np.linspace(1.15,1.4,25),
    np.linspace(1.4,1.5,25),
    np.linspace(1.4,1.5, 25)
])

y = np.concatenate([
    np.linspace(-1, 1, 100),
    np.linspace(0, 1, 100),
    np.linspace(0, -1, 100),
    np.linspace(-0.75, 0.75, 50),
    np.linspace(-0.75, -1, 25),
    np.linspace(0.75, 1, 25),
    np.repeat(1,25),
    np.repeat(-1,25),
    np.linspace(-1, -0.8, 25),
    np.linspace(1, 0.8, 25)
])

z = np.array([x,y])

fix, ax = plt.subplots()
ax.scatter(z[0], z[1])
plt.show()
#%%

#%%
shear = np.array([
    [1,1],
    [0,1]
])

z_shear = np.empty([2, len(z[0])])

for col in range(len(z[0])):
    z_shear[:,col] = z[:,col] @ shear

fix, ax = plt.subplots()
ax.scatter(z_shear[0], z_shear[1])
plt.show()
#%%

#%%
z_shear = np.empty([2, len(z[0])])

for i in np.linspace(0,1,10):

    shear = np.array([
        [1, i],
        [0, 1]
    ])

    for col in range(len(z[0])):
        z_shear[:, col] = z[:, col] @ shear

    # # Mention x and y limits to define their range
    # plt.xlim(0, 100)
    # plt.ylim(0, 100)

    # Plotting graph
    plt.scatter(z_shear[0], z_shear[1])
    plt.pause(0.01)

plt.show()
#%%