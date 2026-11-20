(() => {
    "use strict";

    const translations = {
        "ha": {
            "Home": "Gida",
            "The Problem": "Kalubalen",
            "Our Solution": "Yadda NowV Ke Taimakawa",
            "How It Works": "Yadda Ake Aiki",
            "Contact": "Tuntuɓe Mu",
            "Get Started": "Fara Yanzu",
            "CHINA TO NIGERIA · SIMPLIFYING IMPORTS": "DAGA CHINA ZUWA NAJERIYA · SAUƘAƘA SHIGO DA KAYA",
            "Import from China.": "Shigo da Kaya daga China.",
            "Trade with Confidence.": "Yi Ciniki Cikin Tabbaci.",
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV na taimaka wa ’yan kasuwa da masu son fara shigo da kaya su samo kayayyaki daga China cikin aminci da tabbaci. Muna taimaka musu a dukkan matakai: daga nemo amintattun masu samar da kaya da sadarwa da su cikin yarensu, zuwa duba ingancin kaya, tsara biyan kuɗi da jigilar kayayyaki zuwa Najeriya.",
            "Explore How It Works": "Duba Yadda Ake Aiki",
            "talk to": "yi magana da",
            "Try": "Gwada",
            "Live AI Chat": "Tattaunawar AI Kai Tsaye",
            "From Chinese suppliers to Nigerian businesses. One coordinated import journey.": "Daga masu kaya a China zuwa ’yan kasuwa a Najeriya — dukkan matakan shigo da kaya cikin tsari guda.",
            "THE PROBLEM": "KALUBALEN SHIGO DA KAYA",
            "Importing from China": "Shigo da Kaya daga China",
            "Shouldn't Be This": "Bai kamata ya zama",
            "Complicated.": "mai rikitarwa haka ba.",
            "For many Nigerian businesses, importing involves dealing with multiple intermediaries, unfamiliar suppliers, language barriers and disconnected processes. Every step can introduce uncertainty, additional costs and unnecessary delays.": "Ga ’yan kasuwa da dama a Najeriya, shigo da kaya daga China na zuwa da ƙalubale da dama. Daga wahalar samun amintattun masu kaya da matsalolin harshe, zuwa rashin tabbacin ingancin kaya da rikitarwa wajen biyan kuɗi da jigila. Kowanne mataki na iya haifar da ƙarin kuɗi, jinkiri da rashin tabbas.",
            "Unreliable Suppliers": "Masu Samar da Kaya Marasa Aminci",
            "Finding trustworthy manufacturers and suppliers in China can be difficult, especially without reliable local connections.": "Nemo amintattun masana'antu da masu samar da kaya a China na iya zama ƙalubale, musamman ga waɗanda ba su da amintattun abokan hulɗa a can.",
            "Language Barriers": "Matsalolin Harshe",
            "Communicating with Chinese suppliers, negotiating prices and confirming product specifications can be challenging.": "Sadarwa da masu kaya a China, yin ciniki kan farashi da tabbatar da cikakkun bayanan kayayyaki na iya zama da wahala saboda bambancin harshe.",
            "Product Uncertainty": "Rashin Tabbacin Ingancin Kaya",
            "Buyers may struggle to verify product quality, quantities and specifications before goods leave China.": "Masu saye na iya fuskantar matsala wajen tabbatar da inganci, adadi da kuma bayanan kayayyakin da suka saya kafin a tura su daga China.",
            "Payment Risks": "Haɗarin Biyan Kuɗi",
            "Cross-border payments can expose buyers to uncertainty, limited protection and difficulties resolving disputes.": "Biyan kuɗi tsakanin ƙasashe na iya jefa masu saye cikin rashin tabbas, ƙarancin kariya da wahalar warware saɓani idan matsala ta taso.",
            "Fragmented Logistics": "Rarrabuwar Ayyukan Jigila",
            "Sourcing agents, inspectors, cargo handlers and shipping providers often operate independently, making the process difficult to coordinate.": "Masu nemo kaya, masu duba inganci, masu kula da kaya da kamfanonin sufuri galibi suna aiki daban-daban. Wannan na sa haɗa ayyukansu cikin tsari guda ya zama mai wahala.",
            "The Trust Gap": "Rashin Amincewa da Bayyananniyar Mu'amala",
            "Without transparency and coordination, importers can face hidden charges, unexpected delays and costly mistakes.": "Idan babu cikakken bayani da haɗin kai tsakanin masu gudanar da ayyukan shigo da kaya, ’yan kasuwa na iya fuskantar kuɗaɗen ɓoye, jinkirin da ba a zata ba da kurakurai masu tsada.",
            "THE NOWV SOLUTION": "YADDA NOWV KE TAIMAKAWA",
            "One Coordinated Process.": "Dukkan Matakai Cikin Tsari Guda.",
            "From China to Nigeria.": "Daga China zuwa Najeriya.",
            "Discover Our Process": "Gano Yadda Muke Aiki",
            "Supplier Access": "Haɗa Masu Saye da Masu Kaya",
            "Greater Transparency": "Bayyana Bayanai a Sarari",
            "End-to-End Coordination": "Haɗa Dukkan Ayyukan Shigo da Kaya",
            "WHO WE SERVE": "WAƊANDA MUKE HIDIMTAWA",
            "Built for Businesses": "An Ƙera NowV Domin Taimaka wa ’Yan Kasuwa",
            "at Every Stage of": "A Kowane Mataki na",
            "Importing.": "Shigo da Kaya.",
            "Existing Importers": "Masu Shigo da Kaya",
            "Aspiring Importers": "Masu Shirin Fara Shigo da Kaya",
            "Business Partners": "Abokan Hulɗar Kasuwanci",
            "HOW IT WORKS": "YADDA AKE AIKI",
            "From Supplier Search": "Daga Neman Masu Kaya",
            "to": "zuwa",
            "Final Delivery.": "Har Zuwa Isar da Kaya.",
            "Supplier Sourcing": "Nemo Masu Kaya",
            "Communication": "Sadarwa da Masu Kaya",
            "Product Inspection": "Duba Ingancin Kaya",
            "Payment Coordination": "Gudanar da Tsarin Biyan Kuɗi",
            "International Logistics": "Jigilar Kaya ta Ƙasa da Ƙasa",
            "Nigeria Delivery": "Isar da Kaya a Najeriya",
            "WHY NOWV": "ME YA SA ZAƁI NOWV?",
            "More Than Finding Suppliers.": "Fiye da Nemo Masu Kaya Kawai.",
            "Building Trust in Trade.": "Gina Amincewa a Kasuwanci.",
            "Built Around Real Trade": "An Gina shi Bisa Haƙiƙanin Kasuwanci",
            "Transparency First": "Bayyana Bayanai a Sarari",
            "Technology Driven": "Fasaha ce Ke Jagorantar Ayyukanmu",
            "LET'S CONNECT": "MU HAƊU",
            "Ready to Make": "A Shirye Kuke Ku Sa",
            "Importing from China": "Shigo da Kaya daga China",
            "Simpler?": "Ya Zama Mai Sauƙi?",
            "Start a Conversation": "Fara Tattaunawa da Mu",
            "We look forward to hearing from you.": "Muna fatan jin ta bakinku.",
            "Making China–Nigeria trade simpler, safer and more accessible.": "Sauƙaƙa ciniki tsakanin China da Najeriya, tare da inganta aminci da sauƙin gudanar da shi.",
            "Trade with Confidence.": "Yi Ciniki Cikin Tabbaci."
        },

        "yo": {
            "Home": "Ilé",
            "The Problem": "Ìṣòro náà",
            "Our Solution": "Ojútùú Wa",
            "How It Works": "Bí Ó Ṣe Ń Ṣiṣẹ́",
            "Contact": "Kàn Sí Wa",
            "Get Started": "Bẹ̀rẹ̀ Ní Bayi",
            "CHINA TO NIGERIA · SIMPLIFYING IMPORTS": "LÁTI CHINA SÍ NÀÌJÍRÍÀ · ṢÍṢE KÍ GBÍGBÉ Ọjà WỌLẸ̀ RỌRÙN",
            "Import from China.": "Gbé Ọjà Wọlé Láti China.",
            "Trade with Confidence.": "Ṣe Ìṣòwò Pẹ̀lú Ìgbẹ́kẹ̀lé.",
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV ń ran àwọn oníṣòwò Nàìjíríà àti àwọn tó fẹ́ bẹ̀rẹ̀ ní ṣíṣe ìṣòwò lọ́wọ́ láti rí ọjà ní China nípasẹ̀ ètò kan ṣoṣo — láti wíwá àwọn olùpèsè àti ìbánisọ̀rọ̀ pẹ̀lú àwọn ilé iṣẹ́ títí dé àyẹ̀wò ọjà, ètò ìsanwó àti ìfiránṣẹ́.",
            "Explore How It Works": "Wo Bí Ó Ṣe Ń Ṣiṣẹ́",
            "talk to": "bá",
            "Try": "Dán",
            "Live AI Chat": "Ìjíròrò AI Lójú Ẹsẹ̀",
            "THE PROBLEM": "ÌṢÒRO NÁÀ",
            "Importing from China": "Gbigbé Ọjà Wọlé Láti China",
            "Complicated.": "nira tó bẹ́ẹ̀.",
            "Unreliable Suppliers": "Àwọn Olùpèsè Àìgbẹ́kẹ̀lé",
            "Language Barriers": "Ìdènà Èdè",
            "Product Uncertainty": "Àìdánilójú Ọjà",
            "Payment Risks": "Àwọn Ewu Ìsanwó",
            "Fragmented Logistics": "Ètò Ìrìnnà Ọjà Tí Kò So Pọ̀",
            "The Trust Gap": "Àìní Ìgbẹ́kẹ̀lé",
            "THE NOWV SOLUTION": "OJÚTÙÚ NOWV",
            "One Coordinated Process.": "Ètò Kan Tí A So Pọ̀.",
            "From China to Nigeria.": "Láti China Sí Nàìjíríà.",
            "Discover Our Process": "Kọ́ Sí Ipa Ètò Wa",
            "Supplier Access": "Wíwọlé Sí Àwọn Olùpèsè",
            "Greater Transparency": "Ìṣípayá Tó Dára Jù",
            "End-to-End Coordination": "Ìṣọ̀kan Láti Ìbẹ̀rẹ̀ Dé Òpin",
            "WHO WE SERVE": "ÀWỌN TÍ A Ń RAN LỌ́WỌ́",
            "Built for Businesses": "A Ṣe E Fún Àwọn Oníṣòwò",
            "at Every Stage of": "Ní Gbogbo Ìpele",
            "Importing.": "gbígbé ọjà wọlé.",
            "Existing Importers": "Àwọn Tó Ti Ń Gbé Ọjà Wọlé",
            "Aspiring Importers": "Àwọn Tó Fẹ́ Bẹ̀rẹ̀ Gbigbé Ọjà Wọlé",
            "Business Partners": "Àwọn Alábàáṣiṣẹ́pọ̀",
            "HOW IT WORKS": "BÍ Ó ṢE Ń ṢIṢẸ́",
            "From Supplier Search": "Láti Wíwá Olùpèsè",
            "to": "sí",
            "Final Delivery.": "ìfiránṣẹ́ ọjà sí olùrà.",
            "Supplier Sourcing": "Wíwá Olùpèsè",
            "Communication": "Ìbánisọ̀rọ̀",
            "Product Inspection": "Àyẹ̀wò Ọjà",
            "Payment Coordination": "Ètò Ìsanwó",
            "International Logistics": "Ìrìnnà Ọjà Àgbáyé",
            "Nigeria Delivery": "Ìfiránṣẹ́ Ní Nàìjíríà",
            "WHY NOWV": "ÌDÍ TÍ NOWV FI WÀ",
            "More Than Finding Suppliers.": "Ó Ju Wíwá Àwọn Olùpèsè Lọ.",
            "Building Trust in Trade.": "Kíkọ́ Ìgbẹ́kẹ̀lé Nínú Ìṣòwò.",
            "Built Around Real Trade": "A Dá Lórí Ìṣòwò Gidi",
            "Transparency First": "Ìṣípayá Lákọ̀ọ́kọ́",
            "Technology Driven": "Tí Ìmọ̀ Ẹ̀rọ Ń Darí",
            "LET'S CONNECT": "Ẹ JẸ́ KÁ SỌ̀RỌ̀",
            "Ready to Make": "Ṣé O Ṣetán Láti Jẹ́ Kí",
            "Ready to Make Importing from China": "Ṣé o ti múra láti mú kí gbígbé ọjà wọlé láti China",
            "Simpler?": "rọrùn sí i?",
            "Start a Conversation": "Bẹ̀rẹ̀ Ìjíròrò",
            "We look forward to hearing from you.": "A ń retí láti gbọ́ láti ọ̀dọ̀ yín.",
            "Making China–Nigeria trade simpler, safer and more accessible.": "Ṣíṣe ìṣòwò China àti Nàìjíríà ní rọrùn, ní ààbò àti ní ọ̀nà tó rọrùn láti lò.",
            "Trade with Confidence.": "Ṣe Ìṣòwò Pẹ̀lú Ìgbẹ́kẹ̀lé.",
"Importing from China Shouldn't Be This": "Kò yẹ kí gbígbé ọjà wọlé láti China máa",
            "Built for Businesses at Every Stage of": "Fún àwọn oníṣòwò ní gbogbo ìpele ti",
            "From Supplier Search to": "Láti wíwá olùpèsè dé",
        },

        "ig": {
            "Home": "Ụlọ",
            "The Problem": "Nsogbu",
            "Our Solution": "Ngwọta Anyị",
            "How It Works": "Otu O Si Arụ Ọrụ",
            "Contact": "Kpọtụrụ Anyị",
            "Get Started": "Malite Ugbu A",
            "CHINA TO NIGERIA · SIMPLIFYING IMPORTS": "SITE NA CHINA RỤỌ NAIJIRỊA · IME KA MBUBATA NGWONGWO DỊ MFE",
            "Import from China.": "Bubata Ngwongwo Site na China.",
            "Trade with Confidence.": "Na-azụ Ahịa na Ntụkwasị Obi.",
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV na-enyere ndị ọchụnta ego Naijiria na ndị chọrọ ibubata ngwongwo aka ịchọta ngwaahịa na China site n'usoro ọrụ jikọtara ọnụ — site n'ịchọta ndị na-ebubata ngwongwo na iso ụlọ ọrụ na-emepụta ya kparịta ụka ruo nyocha ngwaahịa, ịhazi ịkwụ ụgwọ na ibuga ya.",
            "Explore How It Works": "Lee Otu Ọ Si Arụ Ọrụ",
            "talk to": "gwa",
            "Try": "Nwaa",
            "Live AI Chat": "Mkparịta Ụka AI Ozugbo",
            "THE PROBLEM": "NSOGBU",
            "Importing from China": "Ibutata Ngwongwo Site na China",
            "Complicated.": "mgbagwoju anya otú a.",
            "Unreliable Suppliers": "Ndị Na-ebubata Ngwongwo A Na-atụkwasịghị Obi",
            "Language Barriers": "Ihe Isi Ike Asụsụ",
            "Product Uncertainty": "Enweghị Nkwenye Banyere Ngwaahịa",
            "Payment Risks": "Ihe Ize Ndụ Ịkwụ Ụgwọ",
            "Fragmented Logistics": "Ụgbọ njem Na-enweghị Njikọ",
            "The Trust Gap": "Enweghị Ntụkwasị Obi",
            "THE NOWV SOLUTION": "NGWỌTA NOWV",
            "One Coordinated Process.": "Otu Usoro Ejikọtara Ọnụ.",
            "From China to Nigeria.": "Site na China Ruo Naijiria.",
            "Discover Our Process": "Chọpụta Usoro Anyị",
            "Supplier Access": "Ịnweta Ndị Na-ebubata Ngwongwo",
            "Greater Transparency": "Nghọta Doro Anya Karịa",
            "End-to-End Coordination": "Ijikọ Usoro Site na Mmalite Ruo Ọgwụgwụ",
            "WHO WE SERVE": "NDỊ ANYỊ NA-EJE OZI",
            "Built for Businesses": "E Mere Ya Maka Azụmahịa",
            "at Every Stage of": "N'ọkwa Ọ bụla nke",
            "Importing.": "ibubata ngwongwo.",
            "Existing Importers": "Ndị Na-ebubata Ngwongwo Ugbu A",
            "Aspiring Importers": "Ndị Chọrọ Ịmalite Ibutata Ngwongwo",
            "Business Partners": "Ndị Mmekọ Azụmahịa",
            "HOW IT WORKS": "OTU Ọ SI ARỤ ỌRỤ",
            "From Supplier Search": "Site n'Ịchọ Onye Na-ebubata Ngwongwo",
            "to": "ruo",
            "Final Delivery.": "nnyefe ngwongwo n’aka onye zụrụ ya.",
            "Supplier Sourcing": "Ịchọta Ndị Na-ebubata Ngwongwo",
            "Communication": "Mkparịta Ụka",
            "Product Inspection": "Nyocha Ngwaahịa",
            "Payment Coordination": "Ịhazi Ịkwụ Ụgwọ",
            "International Logistics": "Ụgbọ njem Mba Nile",
            "Nigeria Delivery": "Nnyefe na Naijiria",
            "WHY NOWV": "IHE KPATARA NOWV",
            "More Than Finding Suppliers.": "Ọ Karịrị Ịchọta Ndị Na-ebubata Ngwongwo.",
            "Building Trust in Trade.": "Iwulite Ntụkwasị Obi na Azụmahịa.",
            "Built Around Real Trade": "E Wuru Ya Dabere na Azụmahịa N'ezie",
            "Transparency First": "Nghọta Doro Anya Nke Mbụ",
            "Technology Driven": "Teknụzụ Na-eduzi Ya",
            "LET'S CONNECT": "KA ANYỊ KPAKỌRỊTA",
            "Ready to Make": "Ị Dị Njikere Ime Ka",
            "Ready to Make Importing from China": "Ị dị njikere ime ka ibubata ngwongwo si China",
            "Simpler?": "dị mfe karị?",
            "Start a Conversation": "Malite Mkparịta Ụka",
            "We look forward to hearing from you.": "Anyị na-atụ anya ịnụ olu unu.",
            "Making China–Nigeria trade simpler, safer and more accessible.": "Ime ka azụmahịa China na Naijiria dị mfe, dị nchebe ma dịkwa mfe ịnweta.",
            "Trade with Confidence.": "Na-azụ Ahịa na Ntụkwasị Obi.",
"Importing from China Shouldn't Be This": "Ibutata ngwongwo site na China ekwesịghị ịdị",
            "Built for Businesses at Every Stage of": "Maka azụmahịa n'ọkwa ọ bụla nke",
            "From Supplier Search to": "Site n'ịchọ ndị na-ebubata ngwongwo ruo",
        },

        "zh-CN": {
            "Home": "首页",
            "The Problem": "行业痛点",
            "Our Solution": "我们的解决方案",
            "How It Works": "运作方式",
            "Contact": "联系我们",
            "Get Started": "立即开始",
            "CHINA TO NIGERIA · SIMPLIFYING IMPORTS": "中国到尼日利亚 · 让进口更简单",
            "Import from China.": "从中国进口。",
            "Trade with Confidence.": "安心开展贸易。",
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV 通过整合进口流程，帮助尼日利亚企业和有意从中国进口商品的人士采购产品，涵盖供应商寻找、制造商沟通、商品检验、付款协调和货物交付。",
            "Explore How It Works": "了解运作方式",
            "talk to": "联系",
            "Try": "体验",
            "Live AI Chat": "实时 AI 聊天",
            "THE PROBLEM": "行业痛点",
            "Importing from China": "从中国进口",
            "Complicated.": "复杂。",
            "Unreliable Suppliers": "供应商缺乏可靠性",
            "Language Barriers": "语言障碍",
            "Product Uncertainty": "商品质量不确定",
            "Payment Risks": "付款风险",
            "Fragmented Logistics": "物流环节分散",
            "The Trust Gap": "信任缺口",
            "THE NOWV SOLUTION": "NOWV 解决方案",
            "One Coordinated Process.": "一体化协调流程。",
            "From China to Nigeria.": "从中国到尼日利亚。",
            "Discover Our Process": "了解我们的流程",
            "Supplier Access": "供应商资源",
            "Greater Transparency": "更高透明度",
            "End-to-End Coordination": "端到端协调",
            "WHO WE SERVE": "我们的服务对象",
            "Built for Businesses": "为各类企业打造",
            "at Every Stage of": "覆盖进口的每个阶段",
            "Importing.": "进口的每个阶段。",
            "Existing Importers": "现有进口商",
            "Aspiring Importers": "计划开展进口业务的人士",
            "Business Partners": "商业合作伙伴",
            "HOW IT WORKS": "运作方式",
            "From Supplier Search": "从寻找供应商",
            "to": "到",
            "Final Delivery.": "最终交付。",
            "Supplier Sourcing": "供应商寻找",
            "Communication": "沟通协调",
            "Product Inspection": "商品检验",
            "Payment Coordination": "付款协调",
            "International Logistics": "国际物流",
            "Nigeria Delivery": "尼日利亚境内配送",
            "WHY NOWV": "为什么选择 NOWV",
            "More Than Finding Suppliers.": "不只是寻找供应商。",
            "Building Trust in Trade.": "建立贸易信任。",
            "Built Around Real Trade": "立足真实贸易需求",
            "Transparency First": "透明优先",
            "Technology Driven": "技术驱动",
            "LET'S CONNECT": "联系我们",
            "Ready to Make": "准备好让",
            "Ready to Make Importing from China": "准备好让从中国进口变得",
            "Simpler?": "更简单了吗？",
            "Start a Conversation": "开始沟通",
            "We look forward to hearing from you.": "期待您的联系。",
            "Making China–Nigeria trade simpler, safer and more accessible.": "让中国与尼日利亚之间的贸易更简单、更安全、更便捷。",
            "Trade with Confidence.": "安心开展贸易。",
"Importing from China Shouldn't Be This": "从中国进口不应该如此",
            "Built for Businesses at Every Stage of": "为各类企业打造，覆盖",
            "From Supplier Search to": "从寻找供应商到",
        }
    };


    const extendedTranslations = {
        ha: {
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV na taimaka wa ’yan kasuwa da masu son fara shigo da kaya su samo kayayyaki daga China cikin aminci da tabbaci. Muna taimaka musu a dukkan matakai: daga nemo amintattun masu samar da kaya da sadarwa da su cikin yarensu, zuwa duba ingancin kaya, tsara biyan kuɗi da jigilar kayayyaki zuwa Najeriya.",
            "From Chinese suppliers to Nigerian businesses. One coordinated import journey.": "Daga masu kaya a China zuwa ’yan kasuwa a Najeriya — dukkan matakan shigo da kaya cikin tsari guda.",
            "For many Nigerian businesses, importing involves dealing with multiple intermediaries, unfamiliar suppliers, language barriers and disconnected processes. Every step can introduce uncertainty, additional costs and unnecessary delays.": "Ga ’yan kasuwa da dama a Najeriya, shigo da kaya daga China na zuwa da ƙalubale da dama. Daga wahalar samun amintattun masu kaya da matsalolin harshe, zuwa rashin tabbacin ingancin kaya da rikitarwa wajen biyan kuɗi da jigila. Kowanne mataki na iya haifar da ƙarin kuɗi, jinkiri da rashin tabbas.",
            "Finding trustworthy manufacturers and suppliers in China can be difficult, especially without reliable local connections.": "Nemo amintattun masana'antu da masu samar da kaya a China na iya zama ƙalubale, musamman ga waɗanda ba su da amintattun abokan hulɗa a can.",
            "Communicating with Chinese suppliers, negotiating prices and confirming product specifications can be challenging.": "Sadarwa da masu kaya a China, yin ciniki kan farashi da tabbatar da cikakkun bayanan kayayyaki na iya zama da wahala saboda bambancin harshe.",
            "Buyers may struggle to verify product quality, quantities and specifications before goods leave China.": "Masu saye na iya fuskantar matsala wajen tabbatar da inganci, adadi da kuma bayanan kayayyakin da suka saya kafin a tura su daga China.",
            "Cross-border payments can expose buyers to uncertainty, limited protection and difficulties resolving disputes.": "Biyan kuɗi tsakanin ƙasashe na iya jefa masu saye cikin rashin tabbas, ƙarancin kariya da wahalar warware saɓani idan matsala ta taso.",
            "Sourcing agents, inspectors, cargo handlers and shipping providers often operate independently, making the process difficult to coordinate.": "Masu nemo kaya, masu duba inganci, masu kula da kaya da kamfanonin sufuri galibi suna aiki daban-daban. Wannan na sa haɗa ayyukansu cikin tsari guda ya zama mai wahala.",
            "Without transparency and coordination, importers can face hidden charges, unexpected delays and costly mistakes.": "Idan babu cikakken bayani da haɗin kai tsakanin masu gudanar da ayyukan shigo da kaya, ’yan kasuwa na iya fuskantar kuɗaɗen ɓoye, jinkirin da ba a zata ba da kurakurai masu tsada.",
            "NowV is building a more accessible and transparent way for Nigerian businesses to import from China. Instead of navigating disconnected intermediaries and processes independently, importers can access coordinated support across supplier sourcing, communication, product inspection, payment coordination and international logistics. Our approach combines real-world trade operations with technology to make importing simpler, more transparent and more reliable.": "NowV na gina hanya mafi sauƙi da bayyana gaskiya ga ’yan kasuwar Najeriya wajen shigo da kaya daga China. Maimakon ’yan kasuwa su riƙa hulɗa da dillalai da wakilai daban-daban domin gudanar da kowane mataki da kansu, NowV na haɗa ayyukan nemo masu kaya, sadarwa da su, duba ingancin kaya, tsara biyan kuɗi da jigilar kaya cikin tsari guda. Muna haɗa ayyukan kasuwanci na zahiri da fasaha domin sauƙaƙa shigo da kaya, ƙara bayyana gaskiya da gina amincewa.",
            "Connecting Nigerian buyers with manufacturers and suppliers in China.": "Haɗa masu saye a Najeriya da masana'antu da masu samar da kaya a China.",
            "Bringing more visibility and coordination to the import process.": "Samar da cikakken bayani da ingantaccen haɗin kai a kowane mataki na shigo da kaya.",
            "Connecting the different stages of importing through one coordinated workflow.": "Haɗa dukkan matakan shigo da kaya cikin tsari guda mai sauƙin gudanarwa.",
            "Whether you already import from China or are preparing to place your first order, NowV is designed to make the process more accessible.": "Ko kuna shigo da kaya daga China a yanzu ko kuna shirin yin odarku ta farko, an tsara NowV domin sauƙaƙa muku wannan tsari.",
            "For Nigerian traders and established businesses who already import but need better supplier access, clearer communication, reliable inspection coordination and more transparent logistics.": "Ga ’yan kasuwa da kamfanonin Najeriya da suka riga suka fara shigo da kaya, amma suke buƙatar ingantacciyar hanyar samun masu kaya, sadarwa mafi kyau, ingantaccen tsarin duba kaya da jigila mai bayyana komai a sarari.",
            "For individuals and businesses looking to start importing but lack the supplier connections, experience or confidence to navigate the process independently.": "Ga mutane da ’yan kasuwa masu son fara shigo da kaya, amma ba su da alaƙa da masu kaya, gogewa ko ƙarfin gwiwar gudanar da dukkan tsarin da kansu.",
            "For Chinese suppliers, manufacturers, logistics providers and trade professionals interested in building more accessible China–Nigeria trade connections.": "Ga masu samar da kaya da masana'antun China, kamfanonin jigila da ƙwararrun ’yan kasuwa masu sha'awar bunƙasa alaƙar kasuwanci tsakanin China da Najeriya.",
            "We are building a coordinated import workflow that connects every important stage of sourcing products from China and getting them to Nigeria.": "Muna gina tsari mai haɗa muhimman matakai na shigo da kaya, tun daga samo kayayyaki a China har zuwa isar da su Najeriya.",
            "Identify suitable manufacturers and suppliers in China based on your product requirements.": "Nemo masana'antu da masu samar da kaya a China waɗanda suka dace da buƙatunku.",
            "Coordinate communication, product specifications, quotations and negotiations with suppliers.": "Taimakawa wajen sadarwa da masu kaya, fayyace bayanan kayayyaki, samun farashi da tattaunawar ciniki.",
            "Coordinate physical checks to help verify product quality, specifications and quantities before shipment.": "Tsara duba kaya kai tsaye domin taimakawa wajen tabbatar da inganci, cikakkun bayanai da adadin kaya kafin a tura su.",
            "Facilitate a more transparent payment process between buyers and suppliers, with payment protection being part of our broader vision.": "Taimakawa wajen samar da tsarin biyan kuɗi mai bayyana komai a sarari tsakanin masu saye da masu kaya. Samar da kariya ga kuɗin da aka biya na daga cikin manyan manufofinmu na gaba.",
            "Coordinate cargo consolidation, shipping arrangements and movement of goods from China to Nigeria.": "Tsara haɗa kayayyaki, shirye-shiryen jigila da jigilar kaya daga China zuwa Najeriya.",
            "Coordinate the final stage of the import journey, helping goods reach their intended Nigerian destination.": "Tsara matakin ƙarshe na jigilar kaya domin taimaka musu isa inda aka nufa a Najeriya.",
            "Importing should not require buyers to independently manage a complicated network of suppliers, intermediaries and logistics providers. NowV is focused on bringing greater coordination, visibility and accessibility to the China–Nigeria import journey. By understanding the realities of Nigerian traders and combining that experience with technology, we aim to build a more dependable way to participate in international trade.": "Bai kamata shigo da kaya ya tilasta wa masu saye gudanar da hadadden tsarin masu kaya, dillalai da masu jigila da kansu ba. NowV na mai da hankali kan inganta haɗin kai, bayyana bayanai a sarari da sauƙaƙa tsarin shigo da kaya tsakanin China da Najeriya. Ta hanyar fahimtar ƙalubalen da ’yan kasuwar Najeriya ke fuskanta da haɗa wannan gogewa da fasaha, muna son gina ingantacciyar hanya ta shiga kasuwancin ƙasa da ƙasa.",
            "Grounded in the practical challenges faced by Nigerian importers.": "An gina shi bisa ainihin ƙalubalen da masu shigo da kaya a Najeriya ke fuskanta.",
            "Focused on clearer communication, coordination and visibility.": "Mai da hankali kan ingantacciyar sadarwa, haɗin kai da bayyana bayanai a sarari.",
            "Building toward a more connected and accessible international trade experience.": "Aiki don samar da tsarin kasuwancin ƙasa da ƙasa mai haɗin kai da sauƙin amfani.",
            "Whether you're an existing importer, an aspiring business owner, a Chinese supplier or a potential partner, we'd like to hear from you. Let's build a more accessible and transparent China–Nigeria trade experience together.": "Ko kun riga kun kasance mai shigo da kaya, kuna shirin fara kasuwanci, ku mai samar da kaya ne a China ko abokin hulɗa na gaba, muna son jin ta bakinku. Mu haɗa kai wajen gina tsarin kasuwanci tsakanin China da Najeriya mai sauƙin amfani da bayyana gaskiya.",
            "Have an import enquiry, partnership proposal or investment interest? Get in touch with our team.": "Kuna da tambaya game da shigo da kaya, shawarar haɗin gwiwa ko sha'awar zuba jari? Ku tuntuɓi ƙungiyarmu.",
            "Making China–Nigeria trade simpler, safer and more accessible.": "Sauƙaƙa ciniki tsakanin China da Najeriya, tare da inganta aminci da sauƙin gudanar da shi.",
            "Importing from China Shouldn't Be This": "Shigo da kaya daga China bai kamata ya zama",
            "Built for Businesses at Every Stage of": "An tsara NowV domin taimaka wa ’yan kasuwa a kowane mataki na",
            "From Supplier Search to": "Daga neman masu kaya har zuwa",
            "Ready to Make Importing from China": "A shirye kuke ku sauƙaƙa shigo da kaya daga China",
            "Simpler?": "?",
            "Who We Serve": "Waɗanda Muke Hidimtawa",
            "© 2026 NowV Global. All rights reserved.": "© 2026 NowV Global. An kiyaye duk haƙƙoƙi."
        },
        yo: {
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV ń ran àwọn oníṣòwò Nàìjíríà àti àwọn tó fẹ́ bẹ̀rẹ̀ sí í kó ọjà wọlé lọ́wọ́ láti rí ọjà ní China nípasẹ̀ ètò tó so gbogbo ìgbésẹ̀ pọ̀ — láti wíwá àwọn olùpèsè àti ìbánisọ̀rọ̀ pẹ̀lú àwọn ilé iṣẹ́ títí dé àyẹ̀wò ọjà, ètò ìsanwó àti ìfiránṣẹ́.",
            "From Chinese suppliers to Nigerian businesses. One coordinated import journey.": "Láti ọ̀dọ̀ àwọn olùpèsè China sí àwọn oníṣòwò Nàìjíríà. Ìrìnàjò gbígbé ọjà wọlé kan ṣoṣo tó ní ètò.",
            "For many Nigerian businesses, importing involves dealing with multiple intermediaries, unfamiliar suppliers, language barriers and disconnected processes. Every step can introduce uncertainty, additional costs and unnecessary delays.": "Fún ọ̀pọ̀ àwọn oníṣòwò Nàìjíríà, gbígbé ọjà wọlé túmọ̀ sí bá ọ̀pọ̀ alárinà ṣiṣẹ́, àwọn olùpèsè tí wọn kò mọ̀, ìdènà èdè àti àwọn ìgbésẹ̀ tí kò so pọ̀. Ìgbésẹ̀ kọ̀ọ̀kan lè mú àìdánilójú, owó àfikún àti ìdádúró tí kò pọndandan wá.",
            "Finding trustworthy manufacturers and suppliers in China can be difficult, especially without reliable local connections.": "Wíwá àwọn ilé iṣẹ́ àti olùpèsè tó ṣeé gbẹ́kẹ̀lé ní China lè ṣòro, pàápàá tí kò bá sí àwọn ìbáṣepọ̀ tó ṣeé gbẹ́kẹ̀lé níbẹ̀.",
            "Communicating with Chinese suppliers, negotiating prices and confirming product specifications can be challenging.": "Bíbá àwọn olùpèsè China sọ̀rọ̀, dúnàádúrà lórí iye owó àti fífìdí àwọn àlàyé ọjà múlẹ̀ lè ṣòro.",
            "Buyers may struggle to verify product quality, quantities and specifications before goods leave China.": "Ó lè ṣòro fún àwọn olùrà láti ṣàyẹ̀wò dídára ọjà, iye rẹ̀ àti àwọn àlàyé rẹ̀ kí ọjà tó kúrò ní China.",
            "Cross-border payments can expose buyers to uncertainty, limited protection and difficulties resolving disputes.": "Ìsanwó láàárín àwọn orílẹ̀-èdè lè mú àìdánilójú, ààbò tó kéré àti ìṣòro yíyanjú àríyànjiyàn bá àwọn olùrà.",
            "Sourcing agents, inspectors, cargo handlers and shipping providers often operate independently, making the process difficult to coordinate.": "Àwọn aṣojú wíwá ọjà, àwọn olùṣàyẹ̀wò, àwọn tó ń bójú tó ẹrù àti àwọn ilé iṣẹ́ ìrìnnà sábà máa ń ṣiṣẹ́ lọ́tọ̀ọ̀tọ̀, èyí tó mú kí ó ṣòro láti so iṣẹ́ wọn pọ̀.",
            "Without transparency and coordination, importers can face hidden charges, unexpected delays and costly mistakes.": "Láìsí ìṣípayá àti ìṣọ̀kan, àwọn tó ń gbé ọjà wọlé lè dojú kọ owó tí a fi pamọ́, ìdádúró àìròtẹ́lẹ̀ àti àṣìṣe tó náni lówó.",
            "NowV is building a more accessible and transparent way for Nigerian businesses to import from China. Instead of navigating disconnected intermediaries and processes independently, importers can access coordinated support across supplier sourcing, communication, product inspection, payment coordination and international logistics. Our approach combines real-world trade operations with technology to make importing simpler, more transparent and more reliable.": "NowV ń kọ́ ọ̀nà tó rọrùn sí i àti tó ṣe kedere fún àwọn oníṣòwò Nàìjíríà láti kó ọjà wọlé láti China. Dípò kí àwọn tó ń kó ọjà wọlé máa bójú tó àwọn alárinà àti ìgbésẹ̀ tó yàtọ̀ síra fúnra wọn, wọ́n lè rí ìrànlọ́wọ́ tó so wíwá olùpèsè, ìbánisọ̀rọ̀, àyẹ̀wò ọjà, ètò ìsanwó àti ìrìnnà ọjà àgbáyé pọ̀. A ń so iṣẹ́ òwò gidi pọ̀ mọ́ ìmọ̀ ẹ̀rọ láti mú kí gbígbé ọjà wọlé rọrùn, ṣe kedere sí i, kí ó sì ṣeé gbẹ́kẹ̀lé.",
            "Connecting Nigerian buyers with manufacturers and suppliers in China.": "Sísopọ̀ àwọn olùrà Nàìjíríà mọ́ àwọn ilé iṣẹ́ àti olùpèsè ní China.",
            "Bringing more visibility and coordination to the import process.": "Mú kí ìlànà gbígbé ọjà wọlé túbọ̀ ṣe kedere, kí àwọn ìgbésẹ̀ sì so pọ̀.",
            "Connecting the different stages of importing through one coordinated workflow.": "Sísopọ̀ gbogbo ìpele gbígbé ọjà wọlé sínú ètò iṣẹ́ kan ṣoṣo.",
            "Whether you already import from China or are preparing to place your first order, NowV is designed to make the process more accessible.": "Bóyá o ti ń kó ọjà wọlé láti China tàbí o ń múra láti ṣe àṣẹ ọjà àkọ́kọ́ rẹ, a ṣe NowV láti mú kí ìlànà náà rọrùn sí i.",
            "For Nigerian traders and established businesses who already import but need better supplier access, clearer communication, reliable inspection coordination and more transparent logistics.": "Fún àwọn oníṣòwò àti ilé iṣẹ́ Nàìjíríà tó ti ń kó ọjà wọlé tẹ́lẹ̀, ṣùgbọ́n tí wọ́n nílò ọ̀nà tó dára sí i láti rí àwọn olùpèsè, ìbánisọ̀rọ̀ tó ṣe kedere, ètò àyẹ̀wò tó ṣeé gbẹ́kẹ̀lé àti ìrìnnà ọjà tó ṣe kedere.",
            "For individuals and businesses looking to start importing but lack the supplier connections, experience or confidence to navigate the process independently.": "Fún àwọn ènìyàn àti ilé iṣẹ́ tó fẹ́ bẹ̀rẹ̀ sí í kó ọjà wọlé ṣùgbọ́n tí kò ní ìbáṣepọ̀ pẹ̀lú olùpèsè, ìrírí tàbí ìgboyà láti ṣe gbogbo ìlànà náà fúnra wọn.",
            "For Chinese suppliers, manufacturers, logistics providers and trade professionals interested in building more accessible China–Nigeria trade connections.": "Fún àwọn olùpèsè àti ilé iṣẹ́ China, àwọn olùpèsè iṣẹ́ ìrìnnà àti àwọn ògbóǹtarìgì òwò tó fẹ́ mú kí ìbáṣepọ̀ òwò China àti Nàìjíríà rọrùn sí i.",
            "We are building a coordinated import workflow that connects every important stage of sourcing products from China and getting them to Nigeria.": "A ń kọ́ ètò gbígbé ọjà wọlé tó so gbogbo ìpele pàtàkì pọ̀, láti rí ọjà ní China títí dé gbígbé wọn wá sí Nàìjíríà.",
            "Identify suitable manufacturers and suppliers in China based on your product requirements.": "Wá àwọn ilé iṣẹ́ àti olùpèsè tó bá ohun tí o nílò mu ní China.",
            "Coordinate communication, product specifications, quotations and negotiations with suppliers.": "Ṣètò ìbánisọ̀rọ̀, àwọn àlàyé ọjà, iye owó àti ìjíròrò ìdúnàádúrà pẹ̀lú àwọn olùpèsè.",
            "Coordinate physical checks to help verify product quality, specifications and quantities before shipment.": "Ṣètò àyẹ̀wò ọjà ní ojúkojú láti ṣàyẹ̀wò dídára, àwọn àlàyé àti iye ọjà kí a tó fi ránṣẹ́.",
            "Facilitate a more transparent payment process between buyers and suppliers, with payment protection being part of our broader vision.": "Ràn àwọn olùrà àti olùpèsè lọ́wọ́ láti ní ètò ìsanwó tó ṣe kedere sí i; ààbò ìsanwó sì jẹ́ apá kan nínú èrò ńlá wa.",
            "Coordinate cargo consolidation, shipping arrangements and movement of goods from China to Nigeria.": "Ṣètò ìṣọ̀kan ẹrù, ètò ìrìnnà àti gbígbé ọjà láti China sí Nàìjíríà.",
            "Coordinate the final stage of the import journey, helping goods reach their intended Nigerian destination.": "Ṣètò ìpele ìkẹyìn ìrìnàjò ọjà kí ó lè dé ibi tí a pinnu rẹ̀ ní Nàìjíríà.",
            "Importing should not require buyers to independently manage a complicated network of suppliers, intermediaries and logistics providers. NowV is focused on bringing greater coordination, visibility and accessibility to the China–Nigeria import journey. By understanding the realities of Nigerian traders and combining that experience with technology, we aim to build a more dependable way to participate in international trade.": "Kò yẹ kí gbígbé ọjà wọlé béèrè pé kí àwọn olùrà máa ṣàkóso ètò tó díjú ti àwọn olùpèsè, alárinà àti àwọn olùpèsè ìrìnnà fúnra wọn. NowV ń ṣiṣẹ́ láti mú ìṣọ̀kan, ìṣípayá àti ìrọ̀rùn pọ̀ sí i nínú gbígbé ọjà wọlé láàárín China àti Nàìjíríà. Nípa òye àwọn ìṣòro gidi tí àwọn oníṣòwò Nàìjíríà ń dojú kọ àti sísopọ̀ ìrírí yẹn mọ́ ìmọ̀ ẹ̀rọ, a fẹ́ kọ́ ọ̀nà tó ṣeé gbẹ́kẹ̀lé sí i fún kíkópa nínú òwò àgbáyé.",
            "Grounded in the practical challenges faced by Nigerian importers.": "Ó dá lórí àwọn ìṣòro gidi tí àwọn tó ń kó ọjà wọlé ní Nàìjíríà ń dojú kọ.",
            "Focused on clearer communication, coordination and visibility.": "Ó dojú kọ ìbánisọ̀rọ̀ tó ṣe kedere, ìṣọ̀kan àti ìṣípayá.",
            "Building toward a more connected and accessible international trade experience.": "Kíkọ́ ìrírí òwò àgbáyé tó so pọ̀ sí i tí ó sì rọrùn láti lò.",
            "Whether you're an existing importer, an aspiring business owner, a Chinese supplier or a potential partner, we'd like to hear from you. Let's build a more accessible and transparent China–Nigeria trade experience together.": "Bóyá o ti ń kó ọjà wọlé, o fẹ́ bẹ̀rẹ̀ iṣẹ́ òwò, o jẹ́ olùpèsè China tàbí alábàáṣiṣẹ́pọ̀ ọjọ́ iwájú, a fẹ́ gbọ́ láti ọ̀dọ̀ rẹ. Ẹ jẹ́ ká jọ kọ́ ìrírí òwò China àti Nàìjíríà tó rọrùn sí i tí ó sì ṣe kedere.",
            "Have an import enquiry, partnership proposal or investment interest? Get in touch with our team.": "Ṣé o ní ìbéèrè nípa gbígbé ọjà wọlé, àbá ìfọwọ́sowọ́pọ̀ tàbí ìfẹ́ láti ṣe ìdókòwò? Kàn sí ẹgbẹ́ wa.",
            "Making China–Nigeria trade simpler, safer and more accessible.": "Ṣíṣe kí òwò China àti Nàìjíríà rọrùn sí i, ní ààbò àti ní ọ̀nà tó rọrùn láti lò.",
            "© 2026 NowV Global. All rights reserved.": "© 2026 NowV Global. Gbogbo ẹ̀tọ́ ni a pamọ́."
        },
        ig: {
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV na-enyere azụmahịa Naijiria na ndị chọrọ ibubata ngwongwo aka ịchọta ngwaahịa na China site n'usoro jikọtara ọnụ — site n'ịchọta ndị na-ebubata ngwongwo na iso ndị nrụpụta kparịta ụka ruo nyocha ngwaahịa, ịhazi ịkwụ ụgwọ na nnyefe.",
            "From Chinese suppliers to Nigerian businesses. One coordinated import journey.": "Site n'aka ndị na-ebubata ngwongwo na China ruo n'aka azụmahịa Naijiria. Otu njem mbubata ahaziri nke ọma.",
            "For many Nigerian businesses, importing involves dealing with multiple intermediaries, unfamiliar suppliers, language barriers and disconnected processes. Every step can introduce uncertainty, additional costs and unnecessary delays.": "Maka ọtụtụ azụmahịa Naijiria, ibubata ngwongwo pụtara iso ọtụtụ ndị nnọchi anya, ndị na-ebubata ngwongwo a na-amaghị, nsogbu asụsụ na usoro na-ejikọtaghị ọnụ rụọ ọrụ. Nzọụkwụ ọ bụla nwere ike iweta enweghị ntụkwasị obi, ụgwọ ndị ọzọ na igbu oge na-enweghị isi.",
            "Finding trustworthy manufacturers and suppliers in China can be difficult, especially without reliable local connections.": "Ịchọta ndị nrụpụta na ndị na-ebubata ngwongwo a pụrụ ịtụkwasị obi na China nwere ike isi ike, ọkachasị ma ọ bụrụ na enweghị ezigbo ndị enyi ma ọ bụ ndị mmekọ n'ebe ahụ.",
            "Communicating with Chinese suppliers, negotiating prices and confirming product specifications can be challenging.": "Iso ndị na-ebubata ngwongwo na China kparịta ụka, ịkparịta ọnụahịa na ịkwado nkọwa ngwaahịa nwere ike isi ike.",
            "Buyers may struggle to verify product quality, quantities and specifications before goods leave China.": "Ọ nwere ike isiri ndị na-azụ ahịa ike inyocha ogo ngwaahịa, ọnụọgụ ya na nkọwa ya tupu ngwongwo apụọ na China.",
            "Cross-border payments can expose buyers to uncertainty, limited protection and difficulties resolving disputes.": "Ịkwụ ụgwọ n'etiti mba nwere ike ime ka ndị na-azụ ahịa nwee enweghị ntụkwasị obi, obere nchekwa na nsogbu idozi esemokwu.",
            "Sourcing agents, inspectors, cargo handlers and shipping providers often operate independently, making the process difficult to coordinate.": "Ndị na-achọ ngwaahịa, ndị na-enyocha ya, ndị na-elekọta ibu na ụlọ ọrụ mbupu na-arụkarị ọrụ iche iche, nke na-eme ka o sie ike ijikọ ọrụ ha.",
            "Without transparency and coordination, importers can face hidden charges, unexpected delays and costly mistakes.": "Enweghị nghọta doro anya na nhazi ọrụ nwere ike ime ka ndị na-ebubata ngwongwo zute ụgwọ zoro ezo, igbu oge a na-atụghị anya ya na mmejọ dị oke ọnụ.",
            "NowV is building a more accessible and transparent way for Nigerian businesses to import from China. Instead of navigating disconnected intermediaries and processes independently, importers can access coordinated support across supplier sourcing, communication, product inspection, payment coordination and international logistics. Our approach combines real-world trade operations with technology to make importing simpler, more transparent and more reliable.": "NowV na-ewu ụzọ dị mfe ịnweta ma doo anya maka azụmahịa Naijiria iji bubata ngwongwo na China. Kama ka ndị na-ebubata ngwongwo na-ahazi ndị nnọchi anya na usoro dị iche iche n'onwe ha, ha nwere ike nweta nkwado jikọtara ọnụ n'ịchọta ndị na-ebubata ngwongwo, nkwurịta okwu, nyocha ngwaahịa, ịhazi ịkwụ ụgwọ na njem ibu mba ụwa. Anyị na-ejikọta ọrụ azụmahịa n'ezie na teknụzụ iji mee ka mbubata dị mfe, doo anya ma bụrụ nke a pụrụ ịtụkwasị obi.",
            "Connecting Nigerian buyers with manufacturers and suppliers in China.": "Ijikọ ndị na-azụ ahịa Naijiria na ndị nrụpụta na ndị na-ebubata ngwongwo na China.",
            "Bringing more visibility and coordination to the import process.": "Ime ka usoro mbubata doo anya ma hazie nke ọma.",
            "Connecting the different stages of importing through one coordinated workflow.": "Ijikọ akụkụ dị iche iche nke mbubata n'otu usoro ọrụ ahaziri nke ọma.",
            "Whether you already import from China or are preparing to place your first order, NowV is designed to make the process more accessible.": "Ma ị na-ebubata ngwongwo na China ugbu a ma ọ bụ na-akwado ime iwu mbụ gị, e mere NowV iji mee ka usoro ahụ dịrị gị mfe.",
            "For Nigerian traders and established businesses who already import but need better supplier access, clearer communication, reliable inspection coordination and more transparent logistics.": "Maka ndị ahịa na azụmahịa Naijiria ndị na-ebubata ngwongwo ugbu a mana chọrọ ohere ka mma ịnweta ndị na-ebubata ngwongwo, nkwurịta okwu doro anya, nhazi nyocha a pụrụ ịtụkwasị obi na njem ibu doro anya karị.",
            "For individuals and businesses looking to start importing but lack the supplier connections, experience or confidence to navigate the process independently.": "Maka ndị mmadụ na azụmahịa chọrọ ịmalite ibubata ngwongwo mana enweghị njikọ ndị na-ebubata ngwongwo, ahụmịhe ma ọ bụ obi ike iji duzie usoro ahụ n'onwe ha.",
            "For Chinese suppliers, manufacturers, logistics providers and trade professionals interested in building more accessible China–Nigeria trade connections.": "Maka ndị na-ebubata ngwongwo na China, ndị nrụpụta, ndị na-enye ọrụ njem ibu na ndị ọkachamara azụmahịa chọrọ iwulite njikọ azụmahịa China na Naijiria dị mfe ịnweta.",
            "We are building a coordinated import workflow that connects every important stage of sourcing products from China and getting them to Nigeria.": "Anyị na-ewu usoro mbubata jikọtara ọnụ nke na-ejikọta akụkụ niile dị mkpa site n'ịchọta ngwaahịa na China ruo n'iweta ha na Naijiria.",
            "Identify suitable manufacturers and suppliers in China based on your product requirements.": "Chọpụta ndị nrụpụta na ndị na-ebubata ngwongwo kwesịrị ekwesị na China dabere n'ihe ị chọrọ.",
            "Coordinate communication, product specifications, quotations and negotiations with suppliers.": "Hazie nkwurịta okwu, nkọwa ngwaahịa, ọnụahịa na mkparịta ụka azụmahịa gị na ndị na-ebubata ngwongwo.",
            "Coordinate physical checks to help verify product quality, specifications and quantities before shipment.": "Hazie nyocha ngwaahịa n'onwe ya iji nyere aka kwenye ogo ya, nkọwa ya na ọnụọgụ ya tupu ebuga ya.",
            "Facilitate a more transparent payment process between buyers and suppliers, with payment protection being part of our broader vision.": "Mee ka usoro ịkwụ ụgwọ dị n'etiti ndị na-azụ ahịa na ndị na-ebubata ngwongwo doo anya karị; nchebe ịkwụ ụgwọ bụkwa akụkụ nke nnukwu ọhụụ anyị.",
            "Coordinate cargo consolidation, shipping arrangements and movement of goods from China to Nigeria.": "Hazie ijikọ ibu, atụmatụ mbupu na njem ngwongwo site na China ruo Naijiria.",
            "Coordinate the final stage of the import journey, helping goods reach their intended Nigerian destination.": "Hazie akụkụ ikpeazụ nke njem mbubata iji nyere ngwongwo aka iru ebe e zubere ha na Naijiria.",
            "Importing should not require buyers to independently manage a complicated network of suppliers, intermediaries and logistics providers. NowV is focused on bringing greater coordination, visibility and accessibility to the China–Nigeria import journey. By understanding the realities of Nigerian traders and combining that experience with technology, we aim to build a more dependable way to participate in international trade.": "Ibutata ngwongwo ekwesịghị ịmanye ndị na-azụ ahịa ijikwa netwọkụ siri ike nke ndị na-ebubata ngwongwo, ndị nnọchi anya na ndị na-enye ọrụ njem ibu n'onwe ha. NowV na-elekwasị anya n'iweta nhazi ka mma, nghọta doro anya na ohere dị mfe n'usoro mbubata China na Naijiria. Site n'ịghọta ihe ndị ahịa Naijiria na-eche ihu na ijikọ ahụmịhe ahụ na teknụzụ, anyị chọrọ iwulite ụzọ a pụrụ ịdabere na ya iji sonye n'ahịa mba ụwa.",
            "Grounded in the practical challenges faced by Nigerian importers.": "Dabere n'ihe isi ike ndị na-ebubata ngwongwo na Naijiria na-eche ihu n'ezie.",
            "Focused on clearer communication, coordination and visibility.": "Na-elekwasị anya na nkwurịta okwu doro anya, nhazi na nghọta.",
            "Building toward a more connected and accessible international trade experience.": "Iwulite ahụmịhe azụmahịa mba ụwa jikọtara ọnụ ma dị mfe ịnweta.",
            "Whether you're an existing importer, an aspiring business owner, a Chinese supplier or a potential partner, we'd like to hear from you. Let's build a more accessible and transparent China–Nigeria trade experience together.": "Ma ị bụ onye na-ebubata ngwongwo ugbu a, onye chọrọ ịmalite azụmahịa, onye na-ebubata ngwongwo na China ma ọ bụ onye nwere ike ịbụ onye mmekọ, anyị chọrọ ịnụ n'aka gị. Ka anyị wulite ahụmịhe azụmahịa China na Naijiria dị mfe ịnweta ma doo anya ọnụ.",
            "Have an import enquiry, partnership proposal or investment interest? Get in touch with our team.": "Ị nwere ajụjụ gbasara mbubata, atụmatụ imekọ ihe ọnụ ma ọ bụ mmasị itinye ego? Kpọtụrụ ndị otu anyị.",
            "Making China–Nigeria trade simpler, safer and more accessible.": "Ime ka azụmahịa China na Naijiria dị mfe, dị nchebe ma dịkwa mfe ịnweta.",
            "© 2026 NowV Global. All rights reserved.": "© 2026 NowV Global. Echekwabara ikike niile."
        },
        "zh-CN": {
            "NowV helps Nigerian businesses and aspiring importers source products from China through a coordinated import process — from finding suppliers and communicating with manufacturers to product inspection, payment coordination and delivery.": "NowV 通过整合进口流程，帮助尼日利亚企业及有意从中国进口商品的人士采购产品，涵盖寻找供应商、与制造商沟通、商品检验、付款协调和货物交付。",
            "From Chinese suppliers to Nigerian businesses. One coordinated import journey.": "从中国供应商到尼日利亚企业，一站式协调进口流程。",
            "For many Nigerian businesses, importing involves dealing with multiple intermediaries, unfamiliar suppliers, language barriers and disconnected processes. Every step can introduce uncertainty, additional costs and unnecessary delays.": "对许多尼日利亚企业而言，进口业务需要面对多个中间商、不熟悉的供应商、语言障碍以及彼此脱节的流程。每个环节都可能带来不确定性、额外成本和不必要的延误。",
            "Finding trustworthy manufacturers and suppliers in China can be difficult, especially without reliable local connections.": "寻找值得信赖的中国制造商和供应商可能并不容易，尤其是在缺乏可靠当地人脉的情况下。",
            "Communicating with Chinese suppliers, negotiating prices and confirming product specifications can be challenging.": "与中国供应商沟通、协商价格以及确认产品规格可能面临困难。",
            "Buyers may struggle to verify product quality, quantities and specifications before goods leave China.": "货物离开中国前，买家可能难以核实产品质量、数量和规格。",
            "Cross-border payments can expose buyers to uncertainty, limited protection and difficulties resolving disputes.": "跨境付款可能使买家面临不确定性、保障不足以及争议处理困难等问题。",
            "Sourcing agents, inspectors, cargo handlers and shipping providers often operate independently, making the process difficult to coordinate.": "采购代理、检验人员、货物处理人员和运输服务商往往各自独立运作，导致整个流程难以协调。",
            "Without transparency and coordination, importers can face hidden charges, unexpected delays and costly mistakes.": "缺乏透明度和协调时，进口商可能遭遇隐藏费用、意外延误以及代价高昂的错误。",
            "NowV is building a more accessible and transparent way for Nigerian businesses to import from China. Instead of navigating disconnected intermediaries and processes independently, importers can access coordinated support across supplier sourcing, communication, product inspection, payment coordination and international logistics. Our approach combines real-world trade operations with technology to make importing simpler, more transparent and more reliable.": "NowV 正在为尼日利亚企业打造更便捷、更透明的中国进口方式。进口商无需独自应对彼此分散的中间商和流程，即可获得供应商寻找、沟通、商品检验、付款协调及国际物流等环节的协同支持。我们将实际贸易运营与技术相结合，让进口流程更简单、更透明、更可靠。",
            "Connecting Nigerian buyers with manufacturers and suppliers in China.": "连接尼日利亚买家与中国制造商及供应商。",
            "Bringing more visibility and coordination to the import process.": "让进口流程更加透明、协调。",
            "Connecting the different stages of importing through one coordinated workflow.": "通过统一协调的工作流程连接进口各个环节。",
            "Whether you already import from China or are preparing to place your first order, NowV is designed to make the process more accessible.": "无论您已经从中国进口商品，还是正准备下第一笔订单，NowV 都致力于让整个流程更加便捷。",
            "For Nigerian traders and established businesses who already import but need better supplier access, clearer communication, reliable inspection coordination and more transparent logistics.": "面向已经开展进口业务、但需要更便捷的供应商渠道、更清晰的沟通、可靠的检验协调以及更透明物流服务的尼日利亚贸易商和成熟企业。",
            "For individuals and businesses looking to start importing but lack the supplier connections, experience or confidence to navigate the process independently.": "面向希望开始进口业务，却缺乏供应商资源、经验或独立处理进口流程信心的个人和企业。",
            "For Chinese suppliers, manufacturers, logistics providers and trade professionals interested in building more accessible China–Nigeria trade connections.": "面向希望建立更便捷的中尼贸易联系的中国供应商、制造商、物流服务商及贸易专业人士。",
            "We are building a coordinated import workflow that connects every important stage of sourcing products from China and getting them to Nigeria.": "我们正在构建一套协调一致的进口流程，连接从中国采购商品到将货物运抵尼日利亚的每一个重要环节。",
            "Identify suitable manufacturers and suppliers in China based on your product requirements.": "根据您的产品需求，在中国寻找合适的制造商和供应商。",
            "Coordinate communication, product specifications, quotations and negotiations with suppliers.": "协调与供应商之间的沟通、产品规格确认、报价及商务谈判。",
            "Coordinate physical checks to help verify product quality, specifications and quantities before shipment.": "安排实物检验，帮助确认货物发运前的产品质量、规格和数量。",
            "Facilitate a more transparent payment process between buyers and suppliers, with payment protection being part of our broader vision.": "推动买家与供应商之间更加透明的付款流程；付款保障也是我们长期愿景的一部分。",
            "Coordinate cargo consolidation, shipping arrangements and movement of goods from China to Nigeria.": "协调货物集运、运输安排以及从中国到尼日利亚的货物流转。",
            "Coordinate the final stage of the import journey, helping goods reach their intended Nigerian destination.": "协调进口流程的最后阶段，帮助货物送达尼日利亚的指定目的地。",
            "Importing should not require buyers to independently manage a complicated network of suppliers, intermediaries and logistics providers. NowV is focused on bringing greater coordination, visibility and accessibility to the China–Nigeria import journey. By understanding the realities of Nigerian traders and combining that experience with technology, we aim to build a more dependable way to participate in international trade.": "进口不应要求买家独自管理复杂的供应商、中间商和物流服务网络。NowV 致力于提升中尼进口流程的协调性、透明度和便利性。通过了解尼日利亚贸易商面临的实际情况，并将这些经验与技术相结合，我们希望打造更可靠的国际贸易参与方式。",
            "Grounded in the practical challenges faced by Nigerian importers.": "立足于尼日利亚进口商面临的实际挑战。",
            "Focused on clearer communication, coordination and visibility.": "注重更清晰的沟通、协调与透明度。",
            "Building toward a more connected and accessible international trade experience.": "致力于打造联系更紧密、参与更便捷的国际贸易体验。",
            "Whether you're an existing importer, an aspiring business owner, a Chinese supplier or a potential partner, we'd like to hear from you. Let's build a more accessible and transparent China–Nigeria trade experience together.": "无论您是现有进口商、计划创业的企业主、中国供应商还是潜在合作伙伴，我们都期待与您交流。让我们共同打造更加便捷、透明的中尼贸易体验。",
            "Have an import enquiry, partnership proposal or investment interest? Get in touch with our team.": "如果您有进口业务咨询、合作提案或投资意向，欢迎联系我们的团队。",
            "Making China–Nigeria trade simpler, safer and more accessible.": "让中国与尼日利亚之间的贸易更简单、更安全、更便捷。",
            "© 2026 NowV Global. All rights reserved.": "© 2026 NowV Global。保留所有权利。"
        }
    };

    Object.keys(extendedTranslations).forEach(language => {
        Object.assign(translations[language], extendedTranslations[language]);
    });

    const selector = document.getElementById("language-select");
    if (!selector) return;

    const normalize = text => text.replace(/\s+/g, " ").trim();
    const originalElements = new WeakMap();
    const originalNodes = new WeakMap();
    const protectedNodes = new WeakSet();

    const textElements = Array.from(
        document.querySelectorAll("p, h1, h2, h3, a, button")
    ).filter(element => element.children.length === 0);

    textElements.forEach(element => {
        originalElements.set(element, element.textContent);

        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT
        );

        let node;
        while ((node = walker.nextNode())) {
            protectedNodes.add(node);
        }
    });

    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT
    );

    const otherNodes = [];
    let currentNode;

    while ((currentNode = walker.nextNode())) {
        if (!protectedNodes.has(currentNode)) {
            originalNodes.set(currentNode, currentNode.nodeValue);
            otherNodes.push(currentNode);
        }
    }

    function applyLanguage(language) {
        const dictionary = translations[language] || {};

        textElements.forEach(element => {
            const original = originalElements.get(element);
            const key = normalize(original);

            element.textContent =
                language === "en" ? original : (dictionary[key] || original);
        });

        otherNodes.forEach(node => {
            const original = originalNodes.get(node);
            const key = normalize(original);

            if (dictionary[key] && language !== "en") {
                const leading = original.match(/^\s*/)[0];
                const trailing = original.match(/\s*$/)[0];

                node.nodeValue = leading + dictionary[key] + trailing;
            } else {
                node.nodeValue = original;
            }
        });

        document.documentElement.lang = language;
        selector.value = language;

        try {
            localStorage.setItem("nowv-language", language);
        } catch (error) {
            // Language switching still works without browser storage.
        }

        const titles = {
            en: "NowV Global | China–Nigeria Import Solutions",
            ha: "NowV Global | Sauƙaƙa Shigo da Kaya daga China zuwa Najeriya",
            yo: "NowV Global | Ojútùú Gbigbé Ọjà Wọlé Láàárín China àti Nàìjíríà",
            ig: "NowV Global | Ngwọta Ibutata Ngwongwo China na Naijiria",
            "zh-CN": "NowV Global | 中国与尼日利亚进口解决方案"
        };

        document.title = titles[language] || titles.en;
    }

    const languageModal = document.getElementById("language-welcome");

    function rememberLanguageChoice(language) {
        applyLanguage(language);

        try {
            localStorage.setItem("nowv-language-selected", "true");
        } catch (error) {
            // Language selection still works without browser storage.
        }

        if (languageModal) {
            languageModal.hidden = true;
            document.body.classList.remove("language-modal-open");
        }
    }

    selector.addEventListener("change", event => {
        rememberLanguageChoice(event.target.value);
    });

    document.querySelectorAll("[data-welcome-language]").forEach(button => {
        button.addEventListener("click", () => {
            rememberLanguageChoice(button.dataset.welcomeLanguage);
        });
    });

    const closeLanguageModal = document.querySelector("[data-welcome-close]");

    if (closeLanguageModal) {
        closeLanguageModal.addEventListener("click", () => {
            rememberLanguageChoice("en");
        });
    }

    let savedLanguage = "en";

    try {
        savedLanguage = localStorage.getItem("nowv-language") || "en";
    } catch (error) {
        savedLanguage = "en";
    }

    // Language is applied after checking whether the visitor has chosen one.

    let hasChosenLanguage = false;

    try {
        hasChosenLanguage =
            localStorage.getItem("nowv-language-selected") === "true";
    } catch (error) {
        hasChosenLanguage = false;
    }

    applyLanguage(
        hasChosenLanguage && translations[savedLanguage]
            ? savedLanguage
            : "en"
    );

    if (!hasChosenLanguage && languageModal) {
        window.addEventListener("load", () => {
            setTimeout(() => {
                languageModal.hidden = false;
                document.body.classList.add("language-modal-open");
            }, 700);
        }, { once: true });
    }
})();
