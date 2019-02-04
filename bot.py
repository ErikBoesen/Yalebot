import modules
import os
import json
import re
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import facebook
import upsidedown


app = Flask(__name__)
F_PATTERN = re.compile('can i get an? (.+) in the chat', flags=re.IGNORECASE | re.MULTILINE)
SUFFIX = '❤️'
GROUP_ID = 1140136552771525
BOOLA_BOOLA = """Bulldog!  Bulldog!
Bow, wow, wow
Eli Yale
Bulldog!  Bulldog!
Bow, wow, wow
Our team can never fail

When the sons of Eli
Break through the line
That is the sign we hail
Bulldog!  Bulldog!
Bow, wow, wow
Eli Yale!"""
UNI_GROUPS = {
    'University of Michigan': 'https://groupme.com/join_group/46781389/hZehS1',
}
ALLOWED_MEMBERS = ["Erik Kieran Boesen","John Yi","Hannah Mendlowitz","Christopher Bowman","Tobi Makinde","Melanie Heller","Akshar Agarwal","Loren Bass Sanford","47 mutual friends including ","Veronica Lee","36 mutual friends including ","Spencer Adler","24 mutual friends including ","JR Im","Jiachen Elizabeth","Jiangda Zhao","Rosie Du","Yiming Zheng","Rinni ThePooh","Maria Mendoza","View 1 recent post","Lucy Harvey","Jeramy Botwe","View 1 recent post","Philos Kim","Wenbo Wu","Alex El Adl","Anoushka Ramkumar","Abinitha Gourabathina","Hannah Hughes","Ashwin Agnihotri","Grace Okeefe","Avery Parr","Shruti Verma","Hassan Osman","Isha Puri","Nick McGowan","Caleb Shi","Siena Cizdziel","View 1 recent post","Sayda Martinez","Anna Quinlan","View 1 recent post","Riley Stanford-Hill","Meera Desai","Roshni Padhi","Rajat Doshi","Malaika Thiam-Bockman","Jennie Miller","Ryan Li","Michal Lewkowicz","Hamilton Wan","View 1 recent post","Maya May","Candy Yang","Asher Noel","Stella Ng","Carson Swank","Claire Donnellan","Eden Gorevoy","Bayan Galal","Shayaan Subzwari","Emma Lilly","Thomas Riegels","Isabella Hay","View 1 recent post","Sindhura Siddapureddy","Brandon Zhu","Candy Lucero","Richard Hausman","Eleanor Norman","Tristan Pinto","Anahi Gonzalez","Yarani Gonzalez","View 1 recent post","Armaan Kalsi","Yash Bhansali","View 1 recent post","Sophie Collins Arroyo","Josh Mckenzie","Natalie Navarrete","Michaela Markels","Katie Painter","Jacob Schaffer","Blake Bridge","Audrey Whitmer","Elizabeth Pandolpho","JohnCarlo Lignelli","Akio Ho","Kayla Wagonfeld","Joe Wickline","View 1 recent post","Nicolás Domínguez Carrero","Leah Cogguillo","Abdullah Shahzad","View 1 recent post","Nick Phillips","Miranda Margulis-Ohnuma","Shudipto Wahed","Jake Schramm","Carolyn Skotz","Giselle Fisher","Joji Baratelli","Cole Donhauser","Cavan Walsh","Itamar Fayler","Grace Lam","Whitney Bowen","Elle Hartje","Ben Scher","Rakel Tanibajeva","Sameeran Das","View 1 recent post","Katie Taylor","Halli Watson","Caroline Reiner","View 1 recent post","Emme Zhou","Alex Wang","Kosuke Tominaga","Owen PH","Olivia Summons","View 1 recent post","Annette Lee","Lindsey Wagner","Ry Walker","Justin Ferrugia","Clay Jamieson","Siow Yee Xian","Mariana Vargas","Katelin Zhou","Atarah Anbar","Katherine Sylvester","Laurel Humphreys","Aram Russell","Robby Hill","Yoony Kim","Daniel Mertus","Cameron Germe","View 1 recent post","Nicholas Davies","Eugene Yu Jun Shen","Yilin Chen","Eli Ablow Measelle","Daniella Shear","Kamsi Adichie","Dwaha Daud","Melanie Landesberg","John Harrington","Christopher Nathan","Iman Iftikhar","Skyler Wilson","Lukas Flippo","Melody Parker","Jessica Romero","Joseph Stauff","Ethan Pesikoff","Mathis-Louis Bitton","Chloe Duval","Jami Rzepecki","Connor Lee","Isaac Pross","Mini Babybel","Drew Kuroda","David Jiang","Cameron Freeman","Nandini Erodula","Houcine Jedli","Christian Robles","Adam Marcelo","Anne Gross","Isabel Chomnalez","Gage Green","Andrew Yuan","Sandra Tang","Wenqian Li","Candice Mulinda","Harry Shindika","Michael Min","Hanah Leventhal","George Dalianis","Monika Krasniqi","Teddy Wooding","Simon Rabinowitz","Yuhan Kim","Victoria Gong","Mona Mahadevan","Matt Leone","Luke Miles","David Ewing","Stephanie Hu","Monica Chang","Drake Pike","Alice Geng","Lily Siegel","Claire Fang","Raja Moreno","Kathryn Yeager","Bryant Reese","Dechen Lama","Shira Minsk","James Kim","Cecile Ramin","Melissa Kim","Enyo Adoboe","Clayton Jelsma Pena","Ayanle Nur","Lexie Gardner","Matteo Carrabba","Jun Chong","Nga Nhi","Joy Cheskin","Andrew King","Nino Baghashvili","Delaney Vu","Nyla Williams","Lauren Lee","Sydney Hirsch","Hannah Schupansky","Kassi Correia","Abigail Romero","Reese Johnson","Ife Adeogun","Mykola Sapronov","Izzy Lopez","Lila Brady","Aidan Williams","Calvin Beltran","Yeabsira Degefu","Joe Page","Jocelyn Zhou","Corbyn Foster","Theo Sandstrom","Sarah Tang","Daniel Posner","Miriam Kopyto","Veronica Lee","Jake Slaughter","Donia Elmansy","Leslie Gonzalez","Chase Daneker","David Zhu","Maya Ingram","Ishwar Mukherjee","Victor Del Carpio Gomez","Henry Betts","Alaman Diadhiou","Alex Potter","Phaedra Letrou","Kiersten Goode","Başak Özsaraç","Anna Vetsch","Poorna Balakumar","Michael Connor","Alexandra Gers","Dev Patale","Jessica Whang","Calista Washburn","Ariana Reichler","Cynthia Lin","Alice Zhang","Erkin Asci","Dania Baig","Catherine Zhang","Karla Camacho","Clare Chemery","Claudius Ptolemaeus","Kelli Hines","Verenice Torres","JT Mullins","Maria Gonzalez","Clio Rose","Jaida Morgan","Christine Lee","Wynton Brown","Lila Drew","Sameer Shaikh","Max Schlenker Schlenker","Henry Saul","JP Ditto","Kwaku Acquah","Hoang Le","Bonnie Bostic","Mishka Philizaire","Mykyta Solonko","Casey Tonnies","Hilary Griggs","Anya van Hoogstraten","Ishan Patel","Josephine Shin","Chase Brownstein","Eric Li","Chloe Conaghan","Gigi Yeung","Jessica Wang","Addison Beer","Ivan Šarić","Harrison Muth","Abri Barrett","Lyron Cotingkeh","Julia Grobman","Andy Zhao","Cindy Kuang","Zachary Groz","Dannie Daley","Kameron Duncan","Sebastian Baez","Drew Ward","Alejandro Simon","Samuel Thompson","Patrick Hackler","Melia Young","Doga Unlu","Soyoung Cho","Itai Almogy","Xander Martin","Bryson Wiese","Ben Markert","Brett Mallee","Evelyn Larson","Raphael Berz","Josie Jahng","Courtney DeNaut","Neal Sarin","Sebastian Ibarraran","Alexis KE","Josie Cummings","Michael Wang","Amelia Davidson","Kolya Bough","Jack Monfort","Emmanuel Kibicho","Sonnet Carter","Leah Fahy","Natalie Sangngam","Supriya Weiss","Megan Wu","Se Ri Lee","Julia Wu","Anna de Hostos","Stella Gray","Ivan Foskey Jr.","Dzidedi Azumah","Alan Park","Claire Chang","Tobi Makinde","Benjamin Kotton","Willa Ferrer","Dora Guo","Caitlin Brown","David Foster","Maximilian DeWolf","Ronnie Eytchison","Brian Burlace","Helen Tamrat","Noah Robinson","Keith Calloway","Griffin Wilson","Sarah Flynn","Vanessa Nunez","Lauren Yoon","Ella Attell","Jasselene Paz","Julia Zhukovets","Henry Wagner","Jacob Kaufman-Shalett","Jamie Yeh","Harris To","Christine Li","Gabriel Broome","Doris Chen","Karenna Thomas","Eliza Poggi","Andrew Kornfeld","Sofia Kouri","Julia Hontaruk-Levko","Lauren Williams","Shreya Pathak","Ako Ndefo-Haven","Catherine Xu","Blen Kedir","View 1 recent post","Sophie Kane","Cole Snedeker","Natalia Torres Arsuaga","Jenny Pan","Gloria Lyu","John Chua","Vivian Cheng","Loren Bass Sanford","Kezia Levy","Shlomi Helfgot","Jakob Johannes Volan","Lauren Kim","Hannah Ji","Serena Lin","Liv Aspegren","Ilan Dubler-Furman","Lila Selin","Cameron Janssens","Simon Palmore","Malcolm Keyes","Iman Dancy","Ophelia Pilkinton","Sophie Licostie","Sophia Zhao","Joseph Zhang","Kelly Long","Justin Yazdi","Abigail Leighton","Maya Wilson","Sophie Houston","Jared Shelby","Ian Berlin","Elisabeth Ross","Bianca Beck","Jenny Hong","Luke Bell","Sam Oguntoyinbo","Samantha Ho","Jacky Chen","Harry Keenan","Luke Tillitski","Elizabeth Levie","Matthew Youkilis","郝仪宸","Elana Rothberg","Cooper Newsom","Miguel von Fedak","Kaitlyn Sandor","Ines Chung-Halpern","Riley Meeks","Marlena Raines","Baylina Pu","Tilden Brooks","Kevin Zhong","Jada DeLeon","Preston Boyd","Alice Zhang","Shreyas Hallur","Jordy Mazza","Renee Theodore","Kristie Qiu","Alex Griffith","Ben Jenkins","Daniel Liu","Diana Kulmizev","Natalie Simpson","Samantha Pohly","Lexy Beard","Elizabeth Ol","Michael Ning","Sarah Sadati","Sofia Restrepo","Amber Amparo","Gretchen Bunovsky","Helen Tejada","Mette Køchs Nielsen","Annila Yan","Zoie Stewart","Blake Torres","Vivian Wang","Alex Martin","Lydia Broderick","Maria Antonia Sendas","Ivy Vuong","Kavya Shah","Julia Zheng","Aliza Fisher","Carlos Montreal Brown","Amma Otchere","Sydney Bryant","Charlotte Townley","Grace Parmer","Drew Beckmen","Rebecca Huang","Chirag Kumar","Ella Gol","Amelia Browne","Julianna Gross","Rebecca Umuringa Mironko","Lane Fischer","Kennedy Nduati","Melanie Heller","Nick Jacobson","Martina Roman Durini","Linda Li","Simi Olurin","Sydney Kunkler","Gia-Han Le","View 1 recent post","Mehdi Lacombe","Jaiveer Singh","Yanpeng Wang","Catherine Zheng","Dan Huynh","Bryce Morales","Kevin Xiao","Eliza Kravitz","Logan Ledman","Alicia Alonso","Matthew Thomas","Molly Fallek","Clarisa Merkatz","Nader Granmayeh","John Albright","Connie Tian","Julia Hornstein","Stephen Moody","Daisy Shah","Alison Zerbib","Lucy Santiago","View 1 recent post","Kyle Lee","Eddy Zhong","Amanda Figueroa","Satoshi Yanaizu","Maria Fernanda Pacheco","Olivia Clark","Georgina Dooley","Sarah Tran","Oscar Taperell","Crystal Wang","Michelle Tong","Keneane Belay","Darren K. Liang","Truman Pipestem","Emmett Solomon","Allan Ding","Aria Harris","Mary Ben Apatoff","Neha Middela","Ryan Felner","Danielle Neil","Austin Cheung","Monica Pena","Isaac Scobey-Thal","Avery Brown","Melina Joseph","Sophie Edelstein","Rachel Cifu","Robert Jed Burde","Rachel Blatt","Victoria Lacombe","Thomas Sutter","Orlee Marini-Rapoport","Rhea Shrivastava","Hailey Dykstra","Alexandra Galloway","Leonardo von Mutius","Jennifer Tegegne","Christopher Yoo","Dora Pang","JD Wright","Doris Igrec","Akshar Agarwal","Anya Dhawan","Ben Christensen","Maile Somera","Alex Jin","Patrick Yang","Jack Bosman","Emme Magliato","Jonah Cho","Brandon Sangmin Lee","View 1 recent post","Sebastian Torres","View 1 recent post","Lena Ansari","Kayla Hoovler","Julia Balch","Linda Liu","JoJo Gum","Tilman Phleger","Luke Couch","Claire St. Peter","Olivia Marwell","Jacquelyn Daigneau","Emmet Halm","Elisabeth Moore","Hannah Oblak","Sofia Fusco","Tyler Juffernbruch","Caroline Beit","Rebecca Li","Eric Linh","Nghiem Pham","Vanessa Hu","Pia Gorme","Diana Zhu","Louie Lu","Milo Mallaby","David Lee","Jessica Pan","Mahad Khan","Deniz Ince","Amay Tewari","Richard Luo","Crista Falk","Annie Giman","Ingrid Ellis","Ran Wang","Sandra Temgoua","Charlotte Murphy","Sam Bezilla","Peter Sykes","Daniel Moscoso","Erik Kieran Boesen","Olivia Tucker","Athena Chang","Lea Kim","Andrea Lee","Ben Beckman","Stephen Carrabino","Noel Rockwell","Oren Schweitzer","Juhani Ilves","Oscar ChaoKe Wang","Jacob Slaughter","Rosie Rothschild","Collin Robinson","Marc-Alain Bertoni","Spencer Adler","Leo Egger","Samuel Eshun Danquah","Charlotte Fennell","Madison Hahamy","Grace Menke","Ishani Singh","Isabella Huang","Gaspard Baroudel","Jake Latts","Matt Song","Adrien Rolet","Ariana Christakis","Daniel Gale","Max Hammond","Ayana Yaegashi","Eunice Park","Ellen Qian","Andrew Jones","Esther Seo","Renita Heng","Julian Tamayo","Eddy Ciobanu","Nubia Jackson","Corinne Smith","Reed Srere","Ashleigh Redding","Jill Carrera","Christopher Bowman","Hannah Mendlowitz","John Yi"]

@app.route("/", methods=["POST"])
def webhook():
    """
    Receive callback to URL when message is sent in the group.
    """
    # Retrieve data on that single GroupMe message.
    message = request.get_json()
    text = message["text"]
    print("Message received: %s" % message)
    matches = F_PATTERN.match(message["text"])
    if matches is not None and len(matches.groups()):
        reply(matches.groups()[0] + ' ' + SUFFIX)
    if message["sender_type"] != "bot":
        if text.startswith("!"):
            command, parameters = text[1:].split(" ", 1)
            command = command.lower()
            module = {
                "zalgo": modules.Zalgo,
            }[command]()
            response = module.response()
            if response is not None:
                reply(response)
        if message["text"].lower().startswith("flip"):
            reply(upsidedown.transform(message["text"][5:]))
        if message["text"] == "!vet":
            reply(vetting_report())
        if "bulldog days" in message["text"].lower():
            reply(modules.Countdown().response())
        if "thank" in message["text"].lower() and "yalebot" in message["text"].lower():
            reply("You're welcome! :)")
        if "favorite song" in message["text"].lower():
            reply(BOOLA_BOOLA)
        if "dad" in message["text"].lower():
            new_text = message["text"].strip().replace("dad", "dyd").replace("Dad", "Dyd").replace("DAD", "DYD")
            reply("Hey " + message["name"] + ", did you mean \"" + new_text + "\"?")
    if message["system"]:
        if not message["text"].startswith("Poll '") and message["text"].contains("the group") and not message.contains("changed name"):
            name = message["text"].replace(" has rejoined the group", "").replace(" has joined the group", "")
            string = name + " "
            string += "is" if name in ALLOWED_MEMBERS else "is NOT"
            string += " a verified Yale admit according to the official Yale '23 Facebook group."
            reply(string)

    return "ok", 200

def vetting_report():
    """
    Compare list of users in GroupMe with Facebook.
    """
    return "Coming soon!"


def reply(text):
    """
    Reply in chat.
    """
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": os.environ["BOT_ID"],
        "text": text,
    }
    request = Request(url, urlencode(data).encode())
    response = urlopen(request).read().decode()
    print("Response after message send: %s" % response)

def vet_user(name: str):
    """
    Check Facebook to determine if user is part of the Yale '23 group.
    """
    os.environ['FACEBOOK_TOKEN']

if __name__ == "__main__":
    print(modules.Countdown().response())
    print(modules.Zalgo().response("Test zalgo"))
