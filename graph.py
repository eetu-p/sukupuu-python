import graphviz
import service
from models import GraphCustomization

def create_graph(
        file_name: str = "testipuu",
        style: GraphCustomization = GraphCustomization()
):

    # TODO: Anna käyttäjän valita, käytetäänkö suuntanuolia (Digraph) 
    # vai ei (Graph).
    dot = graphviz.Graph(
        "sukupuu", 
        filename = file_name,
        node_attr = {
            "fillcolor": style.fill_color, 
            "shape": style.shape,
            "fontcolor": style.font_color,
            "fontname": style.font_name,
            "fontsize": style.font_size,
            "height": style.height,
            "shape": style.shape,
            "style": "filled",
            "width": style.width
        }
    )

    all_persons = service.fetch_all_persons()
    all_families = service.fetch_all_families()
    all_relationships = service.fetch_all_relationships()

    print(all_persons, all_families, all_relationships)

    for relationship in all_relationships:
        family_name = "family" + str(relationship.family_id)
        person = service.fetch_person(relationship.person_id)

        dot.node(
            family_name, 
            "id: " + str(relationship.family_id)
                if style.family_show_id
                else "",
            fillcolor = style.family_fill_color,
            fontcolor = style.family_font_color,
            height = style.family_height,
            shape = style.family_shape,
            width = style.family_width
        )

        # TODO: Tämä if-lauseke on vain sitä varten, että se estää person_name-
        # muuttujan kanssa tapahtuvan virheen. Tarvitaan oikeaoppinen tapa
        # varmistaa, että person- ja family-taulukoissa on ne ID:t, jotka
        # person_family-taulukostakin löytyy.
        if person is not None:
            person_name = ""
            if person.given_name is not None and person.last_name is not None:
                person_name = person.given_name + " " + person.last_name

            dot.node(person_name, f'''<
                <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
                    <TR>
                        <TD>{f'<IMG SRC="{person.image}"/>' 
                                if person.image is not None 
                                else ""}</TD>
                    </TR>
                    <TR><TD><FONT POINT-SIZE='{style.name_font_size}'>{'<B>' if style.name_font_bold else ""}{person_name}{'</B>' if style.name_font_bold else ""}</FONT></TD></TR>
                    {f'<TR><TD>s. {person.date_of_birth}</TD></TR>'
                        if person.date_of_birth is not None
                        else ""}
                    {f'<TR><TD>k. {person.date_of_death}</TD></TR>'
                        if person.date_of_death is not None
                        else ""}
                    {f'<TR><TD>id: {person.id}</TD></TR>'
                        if style.show_id
                        else ""}
                </TABLE>
            >''') 

            if relationship.role == "parent":
                dot.edge(person_name, family_name)
            else:
                dot.edge(family_name, person_name)

    dot.render(directory="graphviz_output_test")