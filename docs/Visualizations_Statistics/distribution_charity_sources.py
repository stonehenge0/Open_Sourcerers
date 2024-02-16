import matplotlib.pyplot as plt
 
 
## Plot shows  which evaluators our charities come from.
# Assigning names and values to the charity evaluators.
names='GiveWell', 'Animal Charity Evaluator', 'Deutsches Zentralinstitut für soziale Fragen', "Giving What We Can"
values=[40,19,294,5]

 
# Assign colors. 
colors = ['#4F6272', '#DD7596','#B7C3F3', "#800080"]

# Set label distances, colors, and labels.
plt.pie(values, labels=names, labeldistance=1.15, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors);
plt.show();