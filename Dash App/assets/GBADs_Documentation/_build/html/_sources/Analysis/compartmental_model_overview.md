# Compartmental herd model

The herd dynamics model is a compartmental model in which herds (livestock populations) are divided by sex and age classes. Each sex class (male and female) is classified into three age groups (neonate, juvenile and adult) resulting in six sex-age groups. The model simulates the herd dynamics based on demographic (birth and death rates) and offtake rates in a monthly time step for one year.

The simulation of the model produces annual production offtakes (live animal, milk, draft power, hides, manure etc.) and their respective monetary values (revenue) based on prices for these production outputs. It also estimates the change in total expenditure on production inputs: feed, labor and animal health care. The revenue and costs from the herd model enable the calculation of gross margins for the simulated populations.

The herd dynamics model is run separately for each species, year, and production system, as these all have different population dynamics. These differences are captured by using different values for the model parameters, listed below. Furthermore, we vary the parameters to reflect different disease states in the population, which we refer to as scenarios. 

The scenarios we use are:
- *Current:* The current scenario for a given species, year, and production system uses parameters informed by available data.
- *Ideal:* The ideal scenario adjusts these parameters to reflect a hypothetical ideal if there were no disease pressure. The ideal scenario includes, among other things, improved growth and fertility rates, zero mortality, and zero health expenditure. The results from this scenario are compared to the current scenario to calculate the overall impact of disease.
- *Zero Mortality:* The zero mortality scenario sets mortality rate to zero while keeping other population dynamics, such as growth and fertility rates, at their current values.
- *Disease-specific:* The impact of an individual disease is estimated by adjusting the ideal parameters to reflect the impact of the disease of interest if it were the only disease in the population. One disease may impact fertility while another impacts growth rate; each of these is run as a separate scenario. The results from these scenarios are compared to the ideal to calculate the impact of each disease of interest.

The parameters of the herd dynamics model include:

**Population dynamics**
- Initial population (number of head) for each of the 6 sex-age groups
- Growth rate from neonate to juvenile and from juvenile to adult
- Fertility rate
- Mortality rates for neonates, juveniles, adult females, and adult males
- Cull rates for adult males and females

**Production Values**
- Liveweight conversion for each of the 6 sex-age groups
- Offtake rates for adult males and adult females
- Carcass yield as % of liveweight
- Lactation
    - Proportion of adult females lactating
	- Lactation duration (days)
	- Average daily milk yield (liters)
	- Monetary value of milk
- Draught (cattle only)
    - Castration rate of adult males
	- Draught usage rate
	- Monetary value of draught per head per day
- Monetary value of live animals for each of the 6 sex-age groups
- Hide production rate
- Monetary value of hides
- Manure production rate for each age group (kg per day)
- Monetary value of manure

**Costs**
- Feed requirements and costs
    - Dry matter feed requirements for each of the 6 sex-age groups (proportion of liveweight)
    - Proportion of livestock keepers that purchase feed
    - Dry matter in feed as proportion of weight
    - Feed cost per kg dry matter
- Cost of labor for livestock keepers per head per month
    - Separate for Cattle, Oxen, and Dairy (cattle only)
- Health expenditure per head per month
    - Preventative care
	- Treatment
- Capital costs
    - Interest rate
	- Infrastructure cost per head