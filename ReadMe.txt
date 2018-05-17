#Veranderingen aan het originele ontwerp
-pubmedRetrieval.py staat los van TextDataprocessing.py, dus er is een extra pythonbestand
-pubchempy wordt gebruikt als package
-Selenium en Beautifulsoup zijn eruit gehaald vanwege het feit dat deze afhankelijk zijn van een constante staat van de pubmed ncbi website (bij een update komen er problemen). Ook wordt de feature niet meer gesupport door ons omdat het cross-browser zou moeten worden gemaakt met if statements of een alternatieve manier die we nou dus niet uit gaan zoeken. De officiele API wordt gebruikt. Jammer tho...