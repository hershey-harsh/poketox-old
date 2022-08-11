from collections import namedtuple

from discord.ext import commands

PokemonEmojis = namedtuple("PokemonEmojis", ("normal"))

servers = PokemonEmojis(
    normal=(
        None,
        721451336847065139,
        721451386751156254,
        721451409526227015,
        721451428501127268,
        721451447178231820,
        721451469164773446,
        721451489293500488,
        721451509501395009,
        721451529407823954,
        721451548546301953,
        721451592963981343,
        721451614321246229,
        721451631606235187,
        721451649146683393,
        721451666699845693,
        721451686249496618,
        721451706239418460,
        848523377646895144,
        980938986916814928,
    ),
    shiny=(
        None,
        722654879901941801,
        722655445558231081,
        722655648998883328,
        722655852099797053,
        724420332022136892,
        724420365300007033,
        724420399760408656,
        724420923620327514,
        730375897114214501,
        730375941494407169,
        730375972582588416,
        730376004333207614,
        739926138297516052,
        739926518066708551,
        739926564837523458,
        746959515726905415,
        746959584807354458,
        848659771678261361,
    ),
)

pokemon = PokemonEmojis(
    normal=(
        None,
        1007375934275473531,
        1007375935407915048,
        1007375936628457482,
        1007375938180358256,
        1007375939551903844,
        1007375940927619083,
        1007375942173331506,
        1007375943767179314,
        1007375945071595590,
        1007375946308911127,
        1007375947755950100,
        1007375949135888546,
        1007375950671007835,
        1007375951727968388,
        1007375953523130478,
        1007375954877874207,
        1007375956043903067,
        1007375957264449676,
        1007375958887628880,
        1007375960242405489,
        1007375961718804570,
        1007375963165831218,
        1007375964365406268,
        1007375965661446214,
        1007375901274673363,
        1007375903023706162,
        1007375904156172338,
        1007375905271844994,
        1007375906236530709,
        1007375907897491506,
        1007375909319348244,
        1007375910669930536,
        1007375911928217670,
        1007375912771272825,
        1007375914079899678,
        1007375915434651688,
        1007375917254979604,
        1007375918496485486,
        1007375919637340261,
        1007375921310867496,
        1007375922581737623,
        1007375923668070400,
        1007375924766965780,
        1007375925983330424,
        1007375927027716276,
        1007375928374083664,
        1007375929527517255,
        1007375930743853056,
        1007375931825987744,
        1007375933000405014,
        1004055893337448519,
        1004055897284300912,
        1004055960165298186,
        1004055961134182451,
        1004055961935282246,
        1004055962526683197,
        1004055963839496283,
        1004055965009723432,
        1004055958059765760,
        1004055959129301144,
        1004055984928477305,
        1004055986534875267,
        1004055987658969118,
        1004055988908867755,
        1004055990141984848,
        1004055982294450206,
        1004055983380762714,
        1004055984215445605,
        1004056002540359741,
        1004056003433725972,
        1004056004364873748,
        1004056005589610544,
        1004056006537515068,
        1004056007535771789,
        1004056000019562507,
        1004056001605029928,
        1004056030956748881,
        1004056031850139688,
        1004056033318150215,
        1004056034471587942,
        1004056035566305311,
        1004056036325466253,
        1004056028578586674,
        1004056029627166781,
        1004056060501446666,
        1004056061663264928,
        1004056062955094117,
        1004056063726854278,
        1004056065446523012,
        1004056066717397062,
        1004056057775149086,
        1004056059197001809,
        1004056106445844611,
        1004056098141122680,
        1004056099487481928,
        1004056100447977622,
        1004056101660151898,
        1004056102939406529,
        1004056103631470604,
        1004056105212727326,
        1007346417058189404,
        1007346418438123611,
        1007346420027760731,
        1007346421810331659,
        1007346422607261878,
        1007346424092041347,
        1007346425383891025,
        1007346426621206548,
        1007346427753664623,
        1007346428944842802,
        1007346429724987434,
        1007346431088140329,
        1007346431847309413,
        1007346434158366880,
        1007346435169210451,
        1007346436523958343,
        1007346437635448882,
        1007346438772097074,
        1007346439841657022,
        1007346441137696810,
        1007346442941255830,
        1007346444384079974,
        1007346445671731221,
        1007346380811030588,
        1007346381888962685,
        1007346385366024273,
        1007346387702251640,
        1007346389073801336,
        1007346390671826954,
        1007346391800090634,
        1007346392852861028,
        1007346394094391356,
        1007346395277180968,
        1007346396665479250,
        1007346397873455254,
        1007346399056236544,
        1007346400188715058,
        1007346401275031633,
        1007346402571067412,
        1007346403644813372,
        1007346404768882888,
        1007346405834235905,
        1007346407201583144,
        1007346408292106240,
        1007346409562980443,
        1007346410859003925,
        1007346412264112238,
        1007346413467861002,
        1007346414625505312,
        1007346415917346836,
        1007346955858477076,
        1007346957154533416,
        1007346958161158299,
        1007346959377506416,
        1007346960723886161,
        1007346961785049128,
        1007346962883956766,
        1007346964079329381,
        1007346965127909483,
        1007346967036301422,
        1007346968135225384,
        1007346969347375195,
        1007346970739871857,
        1007346971415162942,
        1007346973252255844,
        1007346975043223603,
        1007346976351846421,
        1007346977748553799,
        1007346979052982343,
        1007346980684566701,
        1007346982123212870,
        1007346983289225357,
        1007346984140681338,
        1007346985675796501,
        1007346917535142011,
        1007346919779090452,
        1007346921062535228,
        1007346922404716694,
        1007346924195684483,
        1007346925437210645,
        1007346926498349087,
        1007346928243195985,
        1007346930050928711,
        1007346931770593442,
        1007346932911439872,
        1007346933846769714,
        1007346934891155517,
        1007346936426287315,
        1007346937604874391,
        1007346939165151323,
        1007346940893208617,
        1007346942243778600,
        1007346943476891658,
        1007346944391254026,
        1007346945393688720,
        1007346946517782658,
        1007346950892433570,
        1007346952033280082,
        1007346953270603898,
        1007346954646331472,
        1007347291654471691,
        1007347292744982669,
        1007347293793566760,
        1007347294699540551,
        1007347296037523487,
        1007347297673302117,
        1007347298721865810,
        1007347299824980098,
        1007347300923879454,
        1007347302240878593,
        1007347304220602468,
        1007347305189486592,
        1007347306418409542,
        1007347307714445322,
        1007347308523954268,
        1007347309778047136,
        1007347311715819530,
        1007347347342237786,
        1007347349162565702,
        1007347350475382846,
        1007347353583353866,
        1007347354871013446,
        1007347356989141002,
        1007347358582972426,
        1007347360298450944,
        1007347226235900085,
        1007347260792774817,
        1007347262411784312,
        1007347263762350141,
        1007347265993724044,
        1007347268011163708,
        1007347269009416302,
        1007347270087348305,
        1007347271177875598,
        1007347272331296868,
        1007347273572814889,
        1007347275749671012,
        1007347276685000794,
        1007347277746147389,
        1007347278794719362,
        1007347279721664664,
        1007347280707330199,
        1007347281638461440,
        1007347282691231795,
        1007347283668508793,
        1007347284767408189,
        1007347285711126679,
        1007347286864572546,
        1007347287762141224,
        1007347288911384738,
        1007347723135111300,
        1007347724041060494,
        1007347725077074060,
        1007347726146621560,
        1007347727673331762,
        1007347728814178357,
        1007347729690800169,
        1007347731733430352,
        1007347732882673744,
        1007347733742485605,
        1007347735797698671,
        1007347736984694804,
        1007347738180063232,
        1007347739274793010,
        1007347740654706758,
        1007347741912993874,
        1007347743255187526,
        1007347744567984179,
        1007347746040188988,
        1007347747176853656,
        1007347749072687204,
        1007347749852823645,
        1007347751429881946,
        1007347752444899478,
        1007347753262796851,
        1007347754672082995,
        1007347755708063867,
        1007347756752457798,
        1007347757968797807,
        1007347759411638302,
        1007347760896430100,
        1007347761898848339,
        1007347763811463248,
        1007347764801310751,
        1007347642868707420,
        1007347703065358346,
        1007347704097157230,
        1007347705594519552,
        1007347706877972481,
        1007347708161433721,
        1007347709906264064,
        1007347711344902185,
        1007347712766791720,
        1007347714012499999,
        1007347715107209317,
        1007347716474548325,
        1007347717590220900,
        1007347718563307551,
        1007347720102617129,
        1007347721704833104,
        1007348050060124340,
        1007348051452625036,
        1007348052828368996,
        1007348056489984140,
        1007348057647611925,
        1007348059010764850,
        1007348060285829181,
        1007348061636415558,
        1007348229521813535,
        1007348231883206686,
        1007348233284096080,
        1007348235012157523,
        1007348237763629166,
        1007348239139344384,
        1007348240691245187,
        1007348242117304471,
        1007348243648237579,
        1007348261360767066,
        1007348262820397127,
        1007348264628129952,
        1007348266494611557,
        1007348267828379738,
        1007348269191540837,
        1007348270361759905,
        1007348271498395718,
        1007347892941504535,
        1007347949476511815,
        1007347951355572304,
        1007347953654050918,
        1007347955122049106,
        1007347956548124833,
        1007347958116798506,
        1007347959345729556,
        1007347960583041134,
        1007347962067820594,
        1007347963108012217,
        1007347963737145366,
        1007347967709163642,
        1007347968933900408,
        1007347969936326787,
        1007347971135914087,
        1007347972092215306,
        1007347973333725225,
        1007347974831099945,
        1007347976169062459,
        1007347977498665080,
        1007347978555633724,
        1007347979516117224,
        1007347981042843809,
        1007348048277549056,
        1007368955897319444,
        1007368957533106186,
        1007368958611030016,
        1007368959835787374,
        1007370791626739804,
        1007370793342218280,
        1007370794474668043,
        1007371204379815936,
        1007371205977841824,
        1007371207500370060,
        1007371256112357386,
        1007371257429381160,
        1007371258641530910,
        1007371259732037652,
        1007371350119284867,
        1007371352572956732,
        1007371355320242186,
        1007371357253804112,
        1007371359090909204,
        1007371361129336832,
        1007371469711495238,
        1007371471447928842,
        1007371476707577917,
        1007348402952089711,
        1007348404935999528,
        1007348406206865459,
        1007348406823432233,
        1007348408639574097,
        1007348410413744178,
        1007348411730776105,
        1007348413895032862,
        1007348609752256603,
        1007348610670796873,
        1007349476278681670,
        1007349476974923807,
        1007349478635864114,
        1007349480481366056,
        1007350663753244773,
        1007350665443549254,
        1007350667024793670,
        1007350668757061833,
        1007350998647455885,
        1007350999943499912,
        1007351001327603742,
        1007351054310068286,
        1007351055530598410,
        1007351056528851016,
        1007351057996849346,
        1007368864268550194,
        1007368866466373652,
    ),
)

enable_emojis_for = (875526899386953779)

class Sprites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @property
    def status(self):
        return self.bot.user.id in enable_emojis_for

    def __getattr__(self, key):
        if self.status:
            return ""
        else:
            return ""

    def get(self, idx):
        if self.status:
            return f"<:_:{pokemon.normal[idx]}>"
        return ""


async def setup(bot: commands.Bot):
    await bot.add_cog(Sprites(bot))
