import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def critique_site_web(theme, scrapping):
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    # Crée le message en remplaçant les placeholders
    system_message = f"Critique un site web en utilisant un ton passif-agressif et humoristique (paragraphe de 3 lignes). Improvise en fonction du site et ta satire n'aborde QUE le point suivant : {theme}. Tu ne dois pas inventer de fausses informations concernant le site, que de vraies critiques."

    user_message_content = f"voici le contenu scrappé du site :\n{scrapping}"

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0.5,
        system=system_message,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message_content
                    }
                ]
            }
        ]
    )


        # Exemple de réponse de l'API
    api_response = str(message.content)

    # Crop le début et la fin
    text = api_response[len("[TextBlock(text='"):-len("', type='text')]")]

    # Remplacer les caractères échappés
    result = text.replace("\\'", "'").replace('\\"', '"')


    return result

# # Exemple d'utilisation
# theme = "design"
# scrapping = "Le site est plein de couleurs vives et les boutons sont trop gros."
# response = critique_site_web(theme, scrapping)
# print(response)
