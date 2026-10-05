import graphviz
import service
from models import Relationship, GraphCustomization

def create_graph(
        relationships: list[Relationship],
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

    for relationship in relationships:
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
            person_name_display = ""
            if person.given_name is not None and person.last_name is not None:
                person_name_display = person.given_name+" "+person.last_name
            elif person.given_name is not None:
                person_name_display = person.given_name
            elif person.last_name is not None:
                person_name_display = person.last_name

            person_name_internal = "person" + str(person.id)

            dot.node(person_name_internal, f'''<
                <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
                    <TR>
                        <TD>{f'<IMG SRC="{person.image}" SCALE="1" />' 
                                if person.image is not None 
                                else ""}</TD>
                    </TR>
                    <TR><TD><FONT POINT-SIZE='{style.name_font_size}'>{'<B>' if style.name_font_bold else ""}{person_name_display}{'</B>' if style.name_font_bold else ""}</FONT></TD></TR>
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
                dot.edge(person_name_internal, family_name)
            else:
                dot.edge(family_name, person_name_internal)

    dot.render(directory="graphviz_output_test")