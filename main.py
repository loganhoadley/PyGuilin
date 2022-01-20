#testing Seaborn library and its interaction in pycharm
#show() needs to be called in order to explicitly draw the generated plot in the IDE
#matplotlib.pyplot.ion() enables interactive mode, which should serve the final product

import seaborn as sns
import matplotlib as plt

df= sns.load_dataset('penguins')
sns.pairplot(df, hue="species")
plt.pyplot.show()
