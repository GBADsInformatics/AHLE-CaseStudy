# Dynamic population model

The dynamic population model is a compartmental model in which herds (livestock populations) are divided by sex and age classes. Each sex class (male and female) is classified into three age groups (juvenile, sub-adult and adult) resulting in six sex-age groups plus an additional age sex group for castrated adult males where appropriate to the system under investigation. The model simulates the herd dynamics based on demographic (birth and death rates) and offtake rates in a monthly time step for one year.

The simulation of the model produces annual production outputs (live animals, meat, milk, draft power, hides, manure etc.) and their respective monetary values (revenue) based on prices for these production outputs. It also estimates the total expenditure on production inputs, including feed, labour and animal health care, according to the population size and structureThe revenue and costs from the herd model enable the calculation of gross margins for the simulated populations.

The model is run separately for each species, year, and production system, as these all have different population dynamics. These differences are captured by using different values for the model parameters, listed below. Furthermore, we vary the parameters to reflect different disease states in the population, which we refer to as scenarios. 

The scenarios we use are:
- *Current:* The current scenario for a given species, year, and production system uses parameters informed by available data.
- *Ideal:* The ideal scenario adjusts these parameters to reflect a hypothetical ideal if there were no disease pressure. The ideal scenario includes, among other things, improved growth and fertility rates, zero mortality, and zero health expenditure. The results from this scenario are compared to the current scenario to calculate the overall impact of disease.
- *Zero Mortality:* The zero mortality scenario sets mortality rate to zero while keeping other population dynamics, such as growth and fertility rates, at their current values.
- *Disease-specific:* The impact of an individual disease is estimated by adjusting the ideal parameters to reflect the impact of the disease of interest if it were the only disease in the population. One disease may impact fertility while another impacts growth rate; each of these is run as a separate scenario. The results from these scenarios are compared to the ideal to calculate the impact of each disease of interest.

The parameters of the herd dynamics model include:

**Population dynamics**

- Initial population (number of head) for each of the sex-age groups

- The rate at which animals mature from juvenile to sub-adult and sub-adult to adult (i.e. the number of months they spend in each age group.)

- Fertility parameters including average litter size and parturition rate

- Mortality rates for juveniles, sub-adults adult females, and adult males

- Age at which adult males and females are assumed to be culled if not already removed from the herd as offtake or mortality

**Production Values**

*Meat and live animal output parameters*

- Liveweights for each of the sex-age groups

- Offtake rates for all sex-age classes

- Carcass yield as % of liveweight

- Monetary value of live animals for each of the sex-age groups

- Lactation parameters

- Proportion of adult females lactating

- Lactation duration (days)

- Average daily milk yield (liters)

- Monetary value of milk

- Draught power parameters (cattle only)

- Castration rate of adult males

- Average number of draught days worked

- Monetary value of draught per head per day

*Other output parameters*

- Hide production rate

- Monetary value of hides

- Manure production rate for each age group (kg per day)

- Monetary value of manure

**Costs**

- Feed requirements and costs

- Dry matter feed requirements for each of the sex-age groups (proportion of liveweight)

- Proportion of livestock keepers that purchase feed

- Dry matter in feed as proportion of weight

- Feed cost per kg dry matter

- Cost of labor for livestock keepers per head per month

- Separate for Cattle, Oxen, and Dairy (cattle only)

- Health expenditure per head per month

- Preventative care costs

- Treatment costs

- Capital costs

- Interest rate

- Infrastructure cost per head