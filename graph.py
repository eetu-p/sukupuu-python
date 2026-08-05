import graphviz
import database
import service

def create_graph():
    dot = graphviz.Digraph(
        "sukupuu", 
        comment = "Minun sukuni",
        node_attr = {
            "shape": "rectangle",
            "fontcolor": "blue"
        }
    )

    # TODO: Vaihda nämä service-funktiohin
    all_persons = database.get_all_persons()
    all_families = database.get_all_families()
    all_relationships = database.get_all_relationships()

    print(all_persons, all_families, all_relationships)

    for relationship in all_relationships:
        family_name = "family" + str(relationship.family_id)
        person = service.fetch_person(relationship.person_id)

        dot.node(family_name)

        # TODO: Tämä if-lauseke on vain sitä varten, että se estää person_name-
        # muuttujan kanssa tapahtuvan virheen. Tarvitaan oikeaoppinen tapa
        # varmistaa, että person- ja family-taulukoissa on ne ID:t, jotka
        # person_family-taulukostakin löytyy.
        if person is not None:
            person_name = ""
            if person.given_name is not None and person.last_name is not None:
                person_name = person.given_name + " " + person.last_name

            dot.node(person_name, f'''<
                <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0">
                    <TR>
                        <TD>{f'<IMG SRC="{person.image}"/>' 
                                if person.image is not None 
                                else ""}</TD>
                    </TR>
                    <TR><TD><B>{person_name}</B></TD></TR>
                    {f'<TR><TD>s. {person.date_of_birth}</TD></TR>'
                        if person.date_of_birth is not None
                        else ""}
                    {f'<TR><TD>k. {person.date_of_death}</TD></TR>'
                        if person.date_of_death is not None
                        else ""}
                    <TR>
                        <TD>id: {person.id}</TD>
                    </TR>
                </TABLE>
            >''')

            if relationship.role == "parent":
                dot.edge(person_name, family_name)
            else:
                dot.edge(family_name, person_name)

    dot.render(directory="graphviz_output_test")