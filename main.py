# app.py
from fasthtml.common import (
    # These are the HTML components we use in this app
    A,
    AX,
    Button,
    Card,
    CheckboxX,
    Container,
    Div,
    Form,
    Grid,
    Group,
    H1,
    H2,
    Hidden,
    Input,
    Li,
    Main,
    Script,
    Style,
    Textarea,
    Title,
    Titled,
    Ul,
    # These are FastHTML symbols we'll use
    Beforeware,
    fast_app,
    SortableJS,
    fill_form,
    picolink,
    serve,
    # These are from Starlette, Fastlite, fastcore, and the Python stdlib
    FileResponse,
    NotFoundError,
    RedirectResponse,
    patch,
    dataclass)

from models import session, Growers, SeedSource, SubSuccession, Trees
from datetime import date

app, rt = fast_app()

Beforeware(app, rt)


# Home route
@rt("/")
def get():
    title = "LongTrees - Propagation Index"
    return Title(title), Group(Grid(Card(Main(
        Container(H1(title + " Management Dashboard"),
                  Div(A("Manage Growers", href="/growers")),
                  Div(A("Manage Seed Sources", href="/seeds")),
                  Div(A("Manage Trees", href="/trees")),
                  Div(A("Manage Sub Successions", href="/subsuccessions")))))))


# List all growers
@rt("/growers")
def list_growers():
    title = "Growers"
    grower_list = Ul(*[
        Li(f"{g.name} - {g.contact_info} | ",
           A("Edit", href=f"/edit-grower/{g.id}"), " | ",
           A("Delete", href=f"/delete-grower/{g.id}"))
        for g in session.query(Growers).all()
    ])
    return Title(title), Container(
        H1(title), grower_list, Div(A("Add New Grower", href="/add-grower")))


# Add new grower
@rt("/add-grower")
def get_add_grower():
    return Titled(
        "Add Grower",
        Form(Input(name="name", placeholder="Name"),
             Input(name="contact_info", placeholder="Contact Info"),
             Input(name="address", placeholder="Address"),
             Input(name="latitude", placeholder="Latitude", type="number"),
             Input(name="longitude", placeholder="Longitude", type="number"),
             Input(name="group_membership", placeholder="Group Membership"),
             Button("Submit", type="submit"),
             action="/add-grower",
             method="post"))


@rt("/add-grower", methods=["POST"])
def post_add_grower(request):
    new_grower = Growers(name=request.form['name'],
                         contact_info=request.form['contact_info'],
                         address=request.form['address'],
                         latitude=float(request.form['latitude']),
                         longitude=float(request.form['longitude']),
                         group_membership=request.form['group_membership'],
                         joined_at=date.today())
    session.add(new_grower)
    session.commit()
    return RedirectResponse("/growers", status_code=303)


# Edit grower
@rt("/edit-grower/{id}")
def get_edit_grower(id: int):
    g = session.query(Growers).get(id)
    return Titled(
        "Edit Grower",
        Form(Input(name="name", value=g.name, placeholder="Name"),
             Input(name="contact_info",
                   value=g.contact_info,
                   placeholder="Contact Info"),
             Input(name="address", value=g.address, placeholder="Address"),
             Input(name="latitude",
                   value=g.latitude,
                   placeholder="Latitude",
                   type="number"),
             Input(name="longitude",
                   value=g.longitude,
                   placeholder="Longitude",
                   type="number"),
             Input(name="group_membership",
                   value=g.group_membership,
                   placeholder="Group Membership"),
             Button("Submit", type="submit"),
             action=f"/edit-grower/{id}",
             method="post"))


@rt("/edit-grower/{id}", methods=["POST"])
def post_edit_grower(id: int, request):
    grower = session.query(Growers).get(id)
    grower.name = request.form['name']
    grower.contact_info = request.form['contact_info']
    grower.address = request.form['address']
    grower.latitude = float(request.form['latitude'])
    grower.longitude = float(request.form['longitude'])
    grower.group_membership = request.form['group_membership']
    session.commit()
    return RedirectResponse("/growers", status_code=303)


# Delete grower
@rt("/delete-grower/{id}")
def delete_grower(id: int):
    grower = session.query(Growers).get(id)
    session.delete(grower)
    session.commit()
    return RedirectResponse("/growers", status_code=303)


# List all seed sources
@rt("/seeds")
def list_seeds():
    title = "Seed Sources"
    seed_list = Ul(*[
        Li(f"{s.succession_number} - {s.description} | ",
           A("Edit", href=f"/edit-seed/{s.id}"), " | ",
           A("Delete", href=f"/delete-seed/{s.id}"))
        for s in session.query(SeedSource).all()
    ])
    return Title(title), Container(
        H1(title), seed_list, Div(A("Add New Seed Source", href="/add-seed")))


# Add new seed source
@rt("/add-seed")
def get_add_seed():
    return Titled(
        "Add Seed Source",
        Form(Input(name="succession_number", placeholder="Succession Number"),
             Textarea(name="description", placeholder="Description"),
             Input(name="germination_rate",
                   placeholder="Germination Rate",
                   type="number"),
             Input(name="quantity", placeholder="Quantity", type="number"),
             Textarea(name="scarification_instructions",
                      placeholder="Scarification Instructions"),
             Textarea(name="stratification_instructions",
                      placeholder="Stratification Instructions"),
             Input(name="geographic_location",
                   placeholder="Geographic Location"),
             Input(name="supplier", placeholder="Supplier"),
             Input(name="viability_duration",
                   placeholder="Viability Duration"),
             Button("Submit", type="submit"),
             action="/add-seed",
             method="post"))


@rt("/add-seed", methods=["POST"])
def post_add_seed(request):
    new_seed = SeedSource(
        succession_number=request.form['succession_number'],
        description=request.form['description'],
        germination_rate=float(request.form['germination_rate']),
        quantity=int(request.form['quantity']),
        scarification_instructions=request.form['scarification_instructions'],
        stratification_instructions=request.
        form['stratification_instructions'],
        date_added=date.today(),
        seeds_issued=0,
        geographic_location=request.form['geographic_location'],
        supplier=request.form['supplier'],
        viability_duration=request.form['viability_duration'])
    session.add(new_seed)
    session.commit()
    return RedirectResponse("/seeds", status_code=303)


# Edit seed source
@rt("/edit-seed/{id}")
def get_edit_seed(id: int):
    s = session.query(SeedSource).get(id)
    return Titled(
        "Edit Seed Source",
        Form(Input(name="succession_number",
                   value=s.succession_number,
                   placeholder="Succession Number"),
             Textarea(name="description",
                      value=s.description,
                      placeholder="Description"),
             Input(name="germination_rate",
                   value=s.germination_rate,
                   placeholder="Germination Rate",
                   type="number"),
             Input(name="quantity",
                   value=s.quantity,
                   placeholder="Quantity",
                   type="number"),
             Textarea(name="scarification_instructions",
                      value=s.scarification_instructions,
                      placeholder="Scarification Instructions"),
             Textarea(name="stratification_instructions",
                      value=s.stratification_instructions,
                      placeholder="Stratification Instructions"),
             Input(name="geographic_location",
                   value=s.geographic_location,
                   placeholder="Geographic Location"),
             Input(name="supplier", value=s.supplier, placeholder="Supplier"),
             Input(name="viability_duration",
                   value=s.viability_duration,
                   placeholder="Viability Duration"),
             Button("Submit", type="submit"),
             action=f"/edit-seed/{id}",
             method="post"))


@rt("/edit-seed/{id}", methods=["POST"])
def post_edit_seed(id: int, request):
    seed = session.query(SeedSource).get(id)
    seed.succession_number = request.form['succession_number']
    seed.description = request.form['description']
    seed.germination_rate = float(request.form['germination_rate'])
    seed.quantity = int(request.form['quantity'])
    seed.scarification_instructions = request.form[
        'scarification_instructions']
    seed.stratification_instructions = request.form[
        'stratification_instructions']
    seed.geographic_location = request.form['geographic_location']
    seed.supplier = request.form['supplier']
    seed.viability_duration = request.form['viability_duration']
    session.commit()
    return RedirectResponse("/seeds", status_code=303)


# Delete seed source
@rt("/delete-seed/{id}")
def delete_seed(id: int):
    seed = session.query(SeedSource).get(id)
    session.delete(seed)
    session.commit()
    return RedirectResponse("/seeds", status_code=303)


# List all sub successions
@rt("/subsuccessions")
def list_subsuccessions():
    title = "Sub Successions"
    subsuccession_list = Ul(*[
        Li(f"{s.sub_succession_number} - {s.status} | ",
           A("Edit", href=f"/edit-subsuccession/{s.id}"), " | ",
           A("Delete", href=f"/delete-subsuccession/{s.id}"))
        for s in session.query(SubSuccession).all()
    ])
    return Title(title), Container(
        H1(title), subsuccession_list,
        Div(A("Add New Sub Succession", href="/add-subsuccession")))


# Add new sub succession
@rt("/add-subsuccession")
def get_add_subsuccession():
    return Titled(
        "Add Sub Succession",
        Form(Input(name="sub_succession_number",
                   placeholder="Sub Succession Number"),
             Input(name="seed_source_id",
                   placeholder="Seed Source ID",
                   type="number"),
             Input(name="grower_id", placeholder="Grower ID", type="number"),
             Input(name="status", placeholder="Status"),
             Textarea(name="expected_outcome", placeholder="Expected Outcome"),
             Button("Submit", type="submit"),
             action="/add-subsuccession",
             method="post"))


@rt("/add-subsuccession", methods=["POST"])
def post_add_subsuccession(request):
    new_subsuccession = SubSuccession(
        sub_succession_number=request.form['sub_succession_number'],
        seed_source_id=int(request.form['seed_source_id']),
        grower_id=int(request.form['grower_id']),
        created_at=date.today(),
        status=request.form['status'],
        expected_outcome=request.form['expected_outcome'])
    session.add(new_subsuccession)
    session.commit()
    return RedirectResponse("/subsuccessions", status_code=303)


# Edit sub succession
@rt("/edit-subsuccession/{id}")
def get_edit_subsuccession(id: int):
    s = session.query(SubSuccession).get(id)
    return Titled(
        "Edit Sub Succession",
        Form(Input(name="sub_succession_number",
                   value=s.sub_succession_number,
                   placeholder="Sub Succession Number"),
             Input(name="seed_source_id",
                   value=s.seed_source_id,
                   placeholder="Seed Source ID",
                   type="number"),
             Input(name="grower_id",
                   value=s.grower_id,
                   placeholder="Grower ID",
                   type="number"),
             Input(name="status", value=s.status, placeholder="Status"),
             Textarea(name="expected_outcome",
                      value=s.expected_outcome,
                      placeholder="Expected Outcome"),
             Button("Submit", type="submit"),
             action=f"/edit-subsuccession/{id}",
             method="post"))


@rt("/edit-subsuccession/{id}", methods=["POST"])
def post_edit_subsuccession(id: int, request):
    subsuccession = session.query(SubSuccession).get(id)
    subsuccession.sub_succession_number = request.form['sub_succession_number']
    subsuccession.seed_source_id = int(request.form['seed_source_id'])
    subsuccession.grower_id = int(request.form['grower_id'])
    subsuccession.status = request.form['status']
    subsuccession.expected_outcome = request.form['expected_outcome']
    session.commit()
    return RedirectResponse("/subsuccessions", status_code=303)


# Delete sub succession
@rt("/delete-subsuccession/{id}")
def delete_subsuccession(id: int):
    subsuccession = session.query(SubSuccession).get(id)
    session.delete(subsuccession)
    session.commit()
    return RedirectResponse("/subsuccessions", status_code=303)


# List all trees
@rt("/trees")
def list_trees():
    title = "Trees"
    tree_list = Ul(*[
        Li(f"{t.species} - {t.growth_stage} | ",
           A("Edit", href=f"/edit-tree/{t.id}"), " | ",
           A("Delete", href=f"/delete-tree/{t.id}"))
        for t in session.query(Trees).all()
    ])
    return Title(title), Container(H1(title), tree_list,
                                   Div(A("Add New Tree", href="/add-tree")))


# Add new tree
@rt("/add-tree")
def get_add_tree():
    return Titled(
        "Add Tree",
        Form(Input(name="sub_succession_id",
                   placeholder="Sub Succession ID",
                   type="number"),
             Input(name="species", placeholder="Species"),
             Input(name="growth_stage", placeholder="Growth Stage"),
             Input(name="planted_at",
                   placeholder="Planted At (YYYY-MM-DD)",
                   type="date"),
             Input(name="height", placeholder="Height", type="number"),
             Input(name="health_status", placeholder="Health Status"),
             Textarea(name="yield_data", placeholder="Yield Data"),
             Textarea(name="notes", placeholder="Notes"),
             Button("Submit", type="submit"),
             action="/add-tree",
             method="post"))


@rt("/add-tree", methods=["POST"])
def post_add_tree(request):
    new_tree = Trees(sub_succession_id=int(request.form['sub_succession_id']),
                     species=request.form['species'],
                     growth_stage=request.form['growth_stage'],
                     planted_at=request.form['planted_at'],
                     height=float(request.form['height']),
                     health_status=request.form['health_status'],
                     yield_data=request.form['yield_data'],
                     notes=request.form['notes'])
    session.add(new_tree)
    session.commit()
    return RedirectResponse("/trees", status_code=303)


# Edit tree
@rt("/edit-tree/{id}")
def get_edit_tree(id: int):
    t = session.query(Trees).get(id)
    return Titled(
        "Edit Tree",
        Form(Input(name="sub_succession_id",
                   value=t.sub_succession_id,
                   placeholder="Sub Succession ID",
                   type="number"),
             Input(name="species", value=t.species, placeholder="Species"),
             Input(name="growth_stage",
                   value=t.growth_stage,
                   placeholder="Growth Stage"),
             Input(name="planted_at",
                   value=t.planted_at,
                   placeholder="Planted At (YYYY-MM-DD)",
                   type="date"),
             Input(name="height",
                   value=t.height,
                   placeholder="Height",
                   type="number"),
             Input(name="health_status",
                   value=t.health_status,
                   placeholder="Health Status"),
             Textarea(name="yield_data",
                      value=t.yield_data,
                      placeholder="Yield Data"),
             Textarea(name="notes", value=t.notes, placeholder="Notes"),
             Button("Submit", type="submit"),
             action=f"/edit-tree/{id}",
             method="post"))


@rt("/edit-tree/{id}", methods=["POST"])
def post_edit_tree(id: int, request):
    tree = session.query(Trees).get(id)
    tree.sub_succession_id = int(request.form['sub_succession_id'])
    tree.species = request.form['species']
    tree.growth_stage = request.form['growth_stage']
    tree.planted_at = request.form['planted_at']
    tree.height = float(request.form['height'])
    tree.health_status = request.form['health_status']
    tree.yield_data = request.form['yield_data']
    tree.notes = request.form['notes']
    session.commit()
    return RedirectResponse("/trees", status_code=303)


# Delete tree
@rt("/delete-tree/{id}")
def delete_tree(id: int):
    tree = session.query(Trees).get(id)
    session.delete(tree)
    session.commit()
    return RedirectResponse("/trees", status_code=303)


# Serve the app
serve()
