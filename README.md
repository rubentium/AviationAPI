# AviationAPI

#### Requests real-time avaiation data from aviationstack.com through ```avaition_data``` as a json file method and scrapes data off of the json. Use your API key.

##### Note: The default number of flighs that is being considered is 25

| aviation_data Class Method | Description | Arguments | Default | Output Type |
| -------------------------- | ----------- | --------- | ------- | ----------- |
| ```_meth1``` | Creates a dictionary with all airports and assigns an index to each airport and an empty list | ```self``` |   N/A | ```dict``` |
| ```meth2``` | Creates a dictionary with keys as indices and values as airports and returns it | ```self``` | N/A | ```dict``` |
| ```connected_airports``` | Changes 0 to 1 if theres is a connection between a pair of airports and it's recorded in the airport info dictionary (airport connection does not depend on the number of flighs as long as there are(n't) any) | ```self``` | N/A | ```dict``` |
| ```__str__``` | Prints the data | ``self``` | N/A | ```str``` |
| ```matrix``` | Uses connected_airport data to create an adjacency matrix, returns sympy matrix | ```self``` | N/A | ```sympy.Matrix``` |
| ```__jordan_calulator``` | returns  P, J, P^-1 with M = P*J*P^-1 | ```self``` | N/A | ```tuple``` |
| ```connections_bool``` | Returns ```False``` if there are no flights from ```dep (departing)``` airport to ```arr (arriving)``` airport with at most 'layover' number of layovers and if there are, then it returns a ```tuple``` with ```True``` and the minimum number of layovers needed | ```self```, ```dep```, ```arr```, ```layover``` | N/A | ```tuple/bool``` |
| ```departing_from``` | If there are any departing flights from the given ```airport``` then it returns ```True``` else it returns ```False``` | ```self```, ```airport``` | N/A | ```bool``` |
| ```arriving_to``` | If there are any arriving flights to the given ```airport``` then it returns ```True``` else it returns ```False``` | ```self```, ```airport``` | N/A | ```bool``` |
| ```connections``` | Returns a ```list``` of ```tuples``` where the first element is the departure airport, the second is arrival, and the third is the number of layovers if there is no connection between a pair of airports then they wont be included in the list. when ```upto``` is ```False``` it checks the connections between a pair of airports with specifically that number of layovers when it's ```True```, then it gives the pairs that have upto that number of layovers | ```self```, ```layover```, ```upto```, ```func``` | ```upto=False```, ```func=_connection_helper (not subject to change as the workings of the method depends on it)``` | ```list[tuple]``` |
