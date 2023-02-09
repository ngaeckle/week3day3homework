from IPython.display import Image
import requests




# recreate your pokemon class here
class Pokemon:
    def __init__(self, name):
        self.name = name
        self.types = None
        self.weight = None
        self.abilities = None
        self.sprite = None
        self.next_evolution = None
        self.poke_api_call()
        
    def poke_api_call(self):
        # Use the pokemon parameter to make a request to the pokemon
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name}/')

        # if the status code is 200:
        if response.status_code == 200:
            # Get the pokemon's data with the json method
            data = response.json()
            # Pull out the name, weight, types, abilities
            self.name = data['name']

            types = data['types']
            self.types = list(map(lambda x: x['type']['name'], types))

            self.weight = data['weight']

            abilities = data['abilities']
            self.abilities = list(map(lambda x: x['ability']['name'], abilities))
            
            self.sprite = data['sprites']['front_default']

            self.next_evolution = self.get_next_evo(data['species']['url'])

        # if the status code is not 200, print an error message
        else:
            print(f'ERROR, STATUS CODE {response.status_code}')

    #def print_image(self):
    #    display(Image(self.sprite, width = 300))

    def get_next_evo(self, a_url):
        response = requests.get(a_url)
        data = response.json()
        new_response = requests.get(data['evolution_chain']['url'])
        new_data = new_response.json()
        if new_data['chain']['evolves_to']:
            #if can evolve
            # if 1st in chain == self.name
            # return 2nd in chain
            # else
            #   if 2nd in chain == self.name
            #   return 3rd in chain
            #   else
            #   return None
            if new_data['chain']['species']['name'] == self.name:
                return new_data['chain']['evolves_to'][0]['species']['name']
            else:
                if new_data['chain']['evolves_to'][0]['species']['name'] == self.name:
                    return new_data['chain']['evolves_to'][0]['evolves_to'][0]['species']['name']
                else:
                    return None
                    
        else:
            #if cant evolve
            return None


        #return(new_data['chain']['evolves_to'][0]['species']['name'])





    def evolve(self):
        if self.next_evolution:
            self.name = self.next_evolution
            self.poke_api_call()
        else:
            print("This pokemon cant evolve")
        


pokemon1 = Pokemon(7)

print(pokemon1.name)
# pokemon1.print_image()

pokemon1.evolve()
print(pokemon1.name)

pokemon1.evolve()
print(pokemon1.name)



