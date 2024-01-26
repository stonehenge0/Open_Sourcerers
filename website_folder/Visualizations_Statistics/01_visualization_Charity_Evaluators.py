import matplotlib.pyplot as plt
 
 
## Plot shows  which evaluators our charities come from.

# Assigning names and values to the charity evaluators.
names='GiveWell', 'Animal Charity Evaluator ACE', 'Deutsches Zentralinstitut für soziale Fragen DZI',
values=[12,11,3] # This needs to be changed to the actual values later on. 

 
# Assign colors. 
colors = ['#4F6272', '#B7C3F3', '#DD7596']

# Set label distances, colors, and labels.
plt.pie(values, labels=names, labeldistance=1.15, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors);
plt.show();