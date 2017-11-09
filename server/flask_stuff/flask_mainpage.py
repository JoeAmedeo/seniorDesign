from flask import Flask, render_template, request, url_for
from url_documentation import URLDocumentation

app = Flask(__name__)
url_doc = URLDocumentation()




@url_doc.route('/alkene_reactions/<reaction_type>', 'POST', 'Computes the products of a certain alkene reaction with a given alkene', 'A JSON object with the list of products')
@url_doc.set_params('/alkene_reactions/<reaction_type>', [('reaction_type', """ The type of reaction.
\n
It can be: "hydroboration" to yield an anti-Markovnikov alchohol, or "oxymercuration" for a Markovnikov alcohol. \n
"hydrogenation" to yield an alkane. \n
"hx_alkyl_halide", treatment of alkene with hydrogen halide to yield an alkyl halide""", True)], None,                    [('alkene_name', 'IUPAC name of the alkene', True), ('geometric_isomer_notation', '"trans" if we use the cis/trans notation, or the "zusammen" if we use the Z/E notation', False, 'zusammen')])
@url_doc.returns('/alkene_reactions/<reaction_type>', 'This returns a JSON file that contains the products')
@url_doc.json_returns('/alkene_reactions/<reaction_type>', [('products','A list of products, each in IUPAC notation')])
@app.route('/alkene_reactions/<reaction_type>', methods=['POST'])
def alkene_reactions(reaction_type):
    return {'products':[]}

@app.route('/site-map')
def site_map():
    print(dir(url_doc))
    return url_doc.get_docs_string(lambda x: 'url-documentation?id=' + str(x))

@app.route('/url-documentation')
def url_documentation():
    url_id = request.args.get('id')
    return url_doc.get_docs_string_for_id(url_id)
