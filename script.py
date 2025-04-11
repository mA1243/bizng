from bizng.models import db, State, Category, LGA
from bizng import app

def seed_states():
    """Insert all states of Nigeria into the State table."""
    states = [
        "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
        "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa",
        "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
        "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara",
        "Abuja"
    ]

    for state_name in states:
        # Check if the state already exists
        existing_state = State.query.filter_by(name=state_name).first()
        if not existing_state:
            state = State(name=state_name)
            db.session.add(state)

    db.session.commit()
    print("States seeded successfully!")

def seed_categories():
    """Insert categories into the Category table."""
    categories = [
        {"name": "Restaurants", "description": "Places to eat and drink."},
        {"name": "Hotels", "description": "Accommodation and lodging services."},
        {"name": "Supermarkets", "description": "Retail stores for groceries and essentials."},
        {"name": "Pharmacies", "description": "Stores for medical supplies and prescriptions."},
        {"name": "Salons", "description": "Hairdressing and beauty services."},
        {"name": "Gyms", "description": "Fitness and wellness centers."},
        {"name": "Schools", "description": "Educational institutions."},
        {"name": "Hospitals", "description": "Healthcare and medical services."},
        {"name": "Mechanics", "description": "Automobile repair and maintenance services."},
        {"name": "Boutiques", "description": "Clothing and fashion stores."},
    ]

    for category_data in categories:
        # Check if the category already exists
        existing_category = Category.query.filter_by(name=category_data["name"]).first()
        if not existing_category:
            category = Category(name=category_data["name"], description=category_data["description"])
            db.session.add(category)

    db.session.commit()
    print("Categories seeded successfully!")
    
def seed_lgas():
    """Insert all LGAs of Nigeria into the LGA table with corresponding state IDs."""
    lgas = {
    "Abia": ["Aba North", "Aba South", "Arochukwu", "Bende", "Ikwuano", "Isiala Ngwa North", "Isiala Ngwa South", "Isuikwuato", "Obi Ngwa", "Ohafia", "Osisioma", "Ugwunagbo", "Ukwa East", "Ukwa West", "Umuahia North", "Umuahia South", "Umunneochi"],
    "Adamawa": ["Demsa", "Fufore", "Ganye", "Gayuk", "Gombi", "Jada", "Lamurde", "Madagali", "Maiha", "Mayo-Belwa", "Michika", "Mubi North", "Mubi South", "Numan", "Shelleng", "Song", "Toungo", "Yola North", "Yola South"],
    "Akwa Ibom": ["Abak", "Eastern Obolo", "Eket", "Esit Eket", "Essien Udim", "Etim Ekpo", "Etinan", "Ibeno", "Ibesikpo Asutan", "Ibiono-Ibom", "Ika", "Ikono", "Ikot Abasi", "Ikot Ekpene", "Ini", "Itu", "Mbo", "Mkpat-Enin", "Nsit-Atai", "Nsit-Ibom", "Nsit-Ubium", "Obot Akara", "Okobo", "Onna", "Oron", "Oruk Anam", "Udung-Uko", "Ukanafun", "Uruan", "Urue-Offong/Oruko", "Uyo"],
    "Anambra": ["Aguata", "Anambra East", "Anambra West", "Anaocha", "Awka North", "Awka South", "Ayamelum", "Dunukofia", "Ekwusigo", "Idemili North", "Idemili South", "Ihiala", "Njikoka", "Nnewi North", "Nnewi South", "Ogbaru", "Onitsha North", "Onitsha South", "Orumba North", "Orumba South", "Oyi"],
    "Bauchi": ["Alkaleri", "Bauchi", "Bogoro", "Damban", "Darazo", "Dass", "Ganjuwa", "Giade", "Itas/Gadau", "Jama'are", "Katagum", "Kirfi", "Misau", "Ningi", "Shira", "Tafawa Balewa", "Toro", "Warji", "Zaki"],
    "Bayelsa": ["Brass", "Ekeremor", "Kolokuma/Opokuma", "Nembe", "Ogbia", "Sagbama", "Southern Ijaw", "Yenagoa"],
    "Benue": ["Ado", "Agatu", "Apa", "Buruku", "Gboko", "Guma", "Gwer East", "Gwer West", "Katsina-Ala", "Konshisha", "Kwande", "Logo", "Makurdi", "Obi", "Ogbadibo", "Ohimini", "Oju", "Okpokwu", "Otukpo", "Tarka", "Ukum", "Ushongo", "Vandeikya"],
    "Borno": ["Abadam", "Askira/Uba", "Bama", "Bayo", "Biu", "Chibok", "Damboa", "Dikwa", "Gubio", "Guzamala", "Gwoza", "Hawul", "Jere", "Kaga", "Kala/Balge", "Konduga", "Kukawa", "Kwaya Kusar", "Mafa", "Magumeri", "Maiduguri", "Marte", "Mobbar", "Monguno", "Ngala", "Nganzai", "Shani"],
    "Cross River": ["Abi", "Akamkpa", "Akpabuyo", "Bakassi", "Bekwarra", "Biase", "Boki", "Calabar Municipal", "Calabar South", "Etung", "Ikom", "Obanliku", "Obubra", "Obudu", "Odukpani", "Ogoja", "Yakurr", "Yala"],
    "Delta": ["Aniocha North", "Aniocha South", "Bomadi", "Burutu", "Ethiope East", "Ethiope West", "Ika North East", "Ika South", "Isoko North", "Isoko South", "Ndokwa East", "Ndokwa West", "Okpe", "Oshimili North", "Oshimili South", "Patani", "Sapele", "Udu", "Ughelli North", "Ughelli South", "Ukwuani", "Uvwie", "Warri North", "Warri South", "Warri South West"],
    "Ebonyi": ["Abakaliki", "Afikpo North", "Afikpo South", "Ebonyi", "Ezza North", "Ezza South", "Ikwo", "Ishielu", "Ivo", "Izzi", "Ohaozara", "Ohaukwu", "Onicha"],
    "Edo": ["Akoko Edo", "Egor", "Esan Central", "Esan North-East", "Esan South-East", "Esan West", "Etsako Central", "Etsako East", "Etsako West", "Igueben", "Ikpoba Okha", "Oredo", "Orhionmwon", "Ovia North-East", "Ovia South-West", "Owan East", "Owan West", "Uhunmwonde"],
    "Ekiti": ["Ado-Ekiti", "Efon", "Ekiti East", "Ekiti South-West", "Ekiti West", "Emure", "Gbonyin", "Ido-Osi", "Ijero", "Ikere", "Ikole", "Ilejemeje", "Irepodun/Ifelodun", "Ise/Orun", "Moba", "Oye"],
    "Enugu": ["Aninri", "Awgu", "Enugu East", "Enugu North", "Enugu South", "Ezeagu", "Igbo-Etiti", "Igbo-Eze North", "Igbo-Eze South", "Isi Uzo", "Nkanu East", "Nkanu West", "Nsukka", "Oji-River", "Udenu", "Udi", "Uzo-Uwani"],
    "Gombe": ["Akko", "Balanga", "Billiri", "Dukku", "Funakaye", "Gombe", "Kaltungo", "Kwami", "Nafada", "Shongom", "Yamaltu/Deba"],
    "Imo": ["Aboh Mbaise", "Ahiazu Mbaise", "Ikeduru", "Isiala Mbano", "Isu", "Mbaitoli", "Ngor Okpala", "Njaba", "Nkwere", "Obowo", "Oguta", "Ohaji/Egbema", "Oru East", "Oru West", "Owerri Municipal", "Owerri North", "Owerri West", "Umuahia North", "Umuahia South"],
    "Jigawa": ["Auyo", "Babura", "Birnin Kudu", "Buji", "Dutse", "Garki", "Gumel", "Guri", "Gwaram", "Gwiwa", "Hadejia", "Jahun", "Kafin Hausa", "Kazaure", "Kiri Kasama", "Maigatari", "Malam Madori", "Miga", "Ringim", "Roni", "Sule Tankarkar", "Taura", "Yankwashi"],
    "Kaduna": ["Birnin Gwari", "Chikun", "Giwa", "Igabi", "Ikara", "Jaba", "Jema'a", "Kachia", "Kaduna North", "Kaduna South", "Kagarko", "Kajuru", "Lere", "Makarfi", "Sabon Gari", "Soba", "Zaria"],
    "Kano": ["Ajingi", "Albasu", "Bagwai", "Bebeji", "Bichi", "Bunkure", "Dala", "Dambatta", "Dawakin Kudu", "Dawakin Tofa", "Fagge", "Gabasawa", "Garko", "Garun Mallam", "Gezawa", "Gwale", "Kabo", "Kano Municipal", "Karaye", "Kibiya", "Kiru", "Kumbotso", "Kunchi", "Makoda", "Minjibir", "Nasarawa", "Rimin Gado", "Tarauni", "Tofa", "Tsanyawa", "Ungogo", "Warawa", "Wudil"],
    "Katsina": ["Bakori", "Batagarawa", "Batsari", "Baure", "Dandume", "Danmusa", "Danja", "Dutsinma", "Funtua", "Ingawa", "Jibia", "Kankara", "Katsina", "Kurfi", "Kusada", "Mai'adua", "Malumfashi", "Mani", "Mashi", "Matazu", "Musawa", "Rimi", "Sabuwa", "Safana", "Sandamu", "Zango"],
    "Kebbi": ["Aleiro", "Arewa", "Bagudo", "Birnin Kebbi", "Bunza", "Dandi", "Danko-Wasagu", "Gwandu", "Jega", "Kalgo", "Koko-Besse", "Maiyama", "Ngaski", "Sakaba", "Shanga", "Suru", "Wasagu", "Yauri", "Zuru"],
    "Kogi": ["Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", "Ibaji", "Idah", "Igalamela-Odolu", "Ijumu", "Kabba/Bunu", "Kogi", "Mopa-Muro", "Ofu", "Ogori/Mangongo", "Okehi", "Okene", "Olamaboro", "Omala", "Yagba East", "Yagba West"],
    "Kwara": ["Asa", "Baruten", "Ekiti", "Ifelodun", "Ilorin East", "Ilorin South", "Ilorin West", "Irepodun", "Isin", "Kaiama", "Moro", "Offa", "Oke-Ero", "Oyun", "Pategi"],
    "Lagos": ["Ajeromi-Ifelodun", "Alimosho", "Amuwo-Odofin", "Apapa", "Badagry", "Epe", "Ibeju-Lekki", "Ifako-Ijaiye", "Ikorodu", "Kosofe", "Lagos Island", "Lagos Mainland", "Mushin", "Ojo", "Oshodi-Isolo", "Shomolu", "Surulere"],
    "Nasarawa": ["Akwanga", "Awe", "Doma", "Karu", "Keana", "Keffi", "Kokona", "Lafia", "Nasarawa", "Niger", "Obi", "Toto", "Wamba"],
    "Niger": ["Agwara", "Bida", "Bosso", "Chanchaga", "Edati", "Gbako", "Gbagyi", "Katcha", "Kokoro", "Kontagora", "Masha", "Mokwa", "Muya", "Paikoro", "Rafi", "Rijau", "Shiroro", "Suleja", "Tafa", "Wushishi"],
    "Ogun": ["Abeokuta North", "Abeokuta South", "Ado-Odo/Ota", "Ewekoro", "Ifo", "Ijebu East", "Ijebu North", "Ijebu North East", "Ijebu Ode", "Ikenne", "Imeko-Afon", "Ipokia", "Obafemi-Owode", "Odeda", "Odogbolu", "Ogun Waterside", "Remo North", "Shagamu"],
    "Ondo": ["Akoko North-East", "Akoko North-West", "Akoko South-East", "Akoko South-West", "Akure North", "Akure South", "Ese-Odo", "Idanre", "Ifedore", "Ilaje", "Ile-Oluji/Okeigbo", "Irele", "Odigbo", "Oka-Akoko", "Ondo East", "Ondo West", "Ose", "Owo"],
    "Osun": ["Aiyedade", "Aiyedire", "Atakumosa East", "Atakumosa West", "Boluwaduro", "Boripe", "Egbedore", "Ejigbo", "Ife Central", "Ife East", "Ife North", "Ife South", "Ilesa East", "Ilesa West", "Isokan", "Iwo", "Obokun", "Odogbo", "Ola-Oluwa", "Olorunda", "Oriade", "Orolu", "Osogbo"],
    "Oyo": ["Akinyele", "Atiba", "Atigbo", "Egbeda", "Ibadan North", "Ibadan North-East", "Ibadan North-West", "Ibadan South-East", "Ibadan South-West", "Ibarapa Central", "Ibarapa East", "Ibarapa North", "Ido", "Irepo", "Isiala", "Isokan", "Lagelu", "Ona Ara", "Ogbomosho North", "Ogbomosho South", "Olorunsogo", "Oluyole", "Ona Ara", "Oyo East", "Oyo West"],
    "Plateau": ["Barkin Ladi", "Bassa", "Bokkos", "Jos East", "Jos North", "Jos South", "Kanam", "Kanke", "Langtang North", "Langtang South", "Mangu", "Pankshin", "Qua'an Pan", "Riyom", "Shendam", "Wase"],
    "Rivers": ["Ahoada East", "Ahoada West", "Akuku-Toru", "Andoni", "Asari-Toru", "Bonny", "Emohua", "Gokana", "Ikwerre", "Khana", "Obio/Akpor", "Ogba/Egbema/Ndoni", "Ogu/Bolo", "Okrika", "Opobo/Nkoro", "Port Harcourt", "Tai"],
    "Sokoto": ["Binji", "Bodinga", "Dange Shuni", "Gada", "Goronyo", "Gudu", "Illela", "Kebbe", "Kware", "Rabah", "Sabon Birni", "Shagari", "Silame", "Sokoto North", "Sokoto South", "Tambuwal", "Tureta", "Wamako", "Wurno", "Yabo"],
    "Taraba": ["Ardo-Kola", "Bali", "Donga", "Gashaka", "Gumti", "Ibi", "Jalingo", "Karin Lamido", "Kurmi", "Lau", "Sardauna", "Takum", "Ussa", "Wukari", "Yorro", "Zing"],
    "Yobe": ["Bade", "Bursari", "Damaturu", "Fune", "Geidam", "Gujba", "Gulani", "Jakusko", "Karasuwa", "Machina", "Nangere", "Nguru", "Potiskum", "Tarmuwa", "Yunusari", "Zabarmari"],
    "Zamfara": ["Anka", "Bakura", "Birnin Magaji", "Bukkuyum", "Chafe", "Gummi", "Gusau", "Isa", "Kaura Namoda", "Maru", "Shinkafi", "Talata Mafara", "Zurmi"],
    "Abuja": ["Abaji", "Bwari", "Gwagwalada", "Kuje", "Municipal Area Council (AMAC)"]
}

    for state_name, lga_list in lgas.items():
        state = State.query.filter_by(name=state_name).first()
        if state:
            for lga_name in lga_list:
                existing_lga = LGA.query.filter_by(name=lga_name, state_id=state.id).first()
                if not existing_lga:
                    lga = LGA(name=lga_name, state_id=state.id)
                    db.session.add(lga)

    db.session.commit()
    print("LGAs seeded successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_states()
        seed_categories()
        seed_lgas()