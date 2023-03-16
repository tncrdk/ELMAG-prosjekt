import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-2, 8, 0.1)
y = x**2 - x

plt.plot(x, y, label=r"$\Sigma(x)=2 \lambda x$")
# plt.plot(x, y)
plt.legend()
plt.show()
