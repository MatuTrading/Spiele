export const STOCKS=[
 {id:'NRVA',name:'Nerva Systems',sector:'Technologie',price:142,revenue:18500,profit:2700,debt:4800,cap:69000,div:0.004,growth:0.13,vol:0.105,beta:1.35,about:'Cloud-Infrastruktur und KI-Software.'},
 {id:'AION',name:'Aion Robotics',sector:'Technologie',price:86,revenue:7900,profit:850,debt:2200,cap:26800,div:0,growth:0.18,vol:0.13,beta:1.7,about:'Automatisierte Fertigung und humanoide Robotik.'},
 {id:'CYBR',name:'Cybridge Security',sector:'Technologie',price:51,revenue:3800,profit:440,debt:600,cap:14500,div:0,growth:0.16,vol:0.11,beta:1.5,about:'Cybersicherheit für Großunternehmen.'},
 {id:'NORD',name:'NordWerk AG',sector:'Industrie',price:78,revenue:15300,profit:1100,debt:5000,cap:21000,div:0.023,growth:0.045,vol:0.065,beta:1.1,about:'Maschinenbau und smarte Fabriken.'},
 {id:'ARGO',name:'Argo Logistics',sector:'Industrie',price:116,revenue:9200,profit:970,debt:3400,cap:18500,div:0.019,growth:0.055,vol:0.065,beta:0.95,about:'Logistik, Hafeninfrastruktur und Güterverkehr.'},
 {id:'VOLT',name:'Voltix Grid',sector:'Industrie',price:65,revenue:5600,profit:390,debt:2600,cap:11500,div:0.01,growth:0.075,vol:0.08,beta:1.25,about:'Stromnetze und Energiespeicher.'},
 {id:'ALBA',name:'Alba Foods',sector:'Konsum',price:92,revenue:11200,profit:920,debt:2500,cap:18000,div:0.031,growth:0.032,vol:0.045,beta:0.65,about:'Lebensmittel und hochwertige Verbrauchermarken.'},
 {id:'URBN',name:'Urban Avenue',sector:'Konsum',price:58,revenue:4700,profit:310,debt:1200,cap:9800,div:0.009,growth:0.07,vol:0.09,beta:1.3,about:'E-Commerce und urbane Lifestyle-Marken.'},
 {id:'PURE',name:'PureWell Health',sector:'Konsum',price:124,revenue:8300,profit:1120,debt:1750,cap:24000,div:0.017,growth:0.065,vol:0.052,beta:0.8,about:'Medizintechnik und Gesundheitsprodukte.'},
 {id:'SOLR',name:'Solara Renewables',sector:'Energie',price:39,revenue:2900,profit:260,debt:3100,cap:8700,div:0,growth:0.12,vol:0.12,beta:1.45,about:'Solar- und Windstromerzeugung.'},
 {id:'OCEA',name:'OceanBlue Energy',sector:'Energie',price:104,revenue:17400,profit:2350,debt:6200,cap:31500,div:0.038,growth:0.025,vol:0.085,beta:1.05,about:'Diversifizierte Energie- und Offshoreprojekte.'},
 {id:'HELX',name:'Helix BioPower',sector:'Energie',price:73,revenue:6300,profit:510,debt:2900,cap:13100,div:0.016,growth:0.085,vol:0.09,beta:1.2,about:'Bioenergie und nachhaltige Treibstoffe.'}
];
export const DEALS=[
 {id:'pe1',class:'Private Equity',type:'Buyout',name:'Bergmann Präzision',size:85000,commit:85000,risk:3,duration:36,rate:0.16,description:'Profitabler Mittelständler mit neuer Exportstrategie.',benefit:'Marge durch Digitalisierung verbessern',downside:'Hohe Verschuldung und Exportabschwung'},
 {id:'pe2',class:'Private Equity',type:'Growth Equity',name:'Luma HealthTech',size:65000,commit:65000,risk:4,duration:30,rate:0.21,description:'Schnell wachsendes Diagnostikunternehmen.',benefit:'Internationaler Markteintritt',downside:'Hohe Bewertung, unsicherer Produktstart'},
 {id:'pe3',class:'Private Equity',type:'Turnaround',name:'Rhein Components',size:48000,commit:48000,risk:5,duration:24,rate:0.23,description:'Industrie-Zulieferer mit operativem Restrukturierungsbedarf.',benefit:'Kostenprogramm und neues Management',downside:'Starkes Insolvenzrisiko bei Rezession'},
 {id:'pd1',class:'Private Debt',type:'Senior Secured',name:'Hanse Logistik Kredit',size:55000,commit:55000,risk:2,duration:24,rate:0.089,description:'Besicherter Unternehmenskredit für Lagerautomatisierung.',benefit:'Erstrangige Sicherheiten',downside:'Nachfragerückgang im Logistikbereich'},
 {id:'pd2',class:'Private Debt',type:'Unitranche',name:'Alpine Software Loan',size:42000,commit:42000,risk:3,duration:30,rate:0.117,description:'Kredit für ein wachsendes Softwareunternehmen.',benefit:'Attraktiver variabler Kupon',downside:'Refinanzierungs- und Kundenkonzentrationsrisiko'},
 {id:'pd3',class:'Private Debt',type:'Mezzanine',name:'Medico Growth Note',size:35000,commit:35000,risk:5,duration:20,rate:0.155,description:'Nachrangiges Wachstumskapital für Medizintechnik.',benefit:'Hoher Zinssatz bei guter Entwicklung',downside:'Geringe Rückflüsse bei Zahlungsunfähigkeit'},
 {id:'pi1',class:'Infrastruktur',type:'Solarpark',name:'Sonnenfeld Süd',size:70000,commit:70000,risk:2,duration:40,rate:0.105,description:'Solarpark mit langfristiger Stromabnahme.',benefit:'Gut planbare Stromerlöse',downside:'Bauverzögerungen und Wetterrisiko'},
 {id:'pi2',class:'Infrastruktur',type:'Windpark',name:'Nordwind Offshore',size:95000,commit:95000,risk:3,duration:48,rate:0.13,description:'Beteiligung an vier Offshore-Windrädern.',benefit:'Attraktives langfristiges Ertragsprofil',downside:'Lieferkettenprobleme und Wartungskosten'},
 {id:'pi3',class:'Infrastruktur',type:'Rechenzentrum',name:'DataPort Frankfurt',size:110000,commit:110000,risk:4,duration:42,rate:0.15,description:'Neues Rechenzentrum für KI-Cloud-Anbieter.',benefit:'Wachsende Nachfrage nach Rechenleistung',downside:'Baukosten, Energiepreise und Auslastung'},
 {id:'re1',class:'Real Estate',type:'Wohnen',name:'Mainufer Residenzen',size:62000,commit:62000,risk:2,duration:42,rate:0.095,description:'Wohnimmobilien mit stabiler Mieterstruktur.',benefit:'Laufende Mieteinnahmen',downside:'Instandhaltung und regulierte Mieten'},
 {id:'re2',class:'Real Estate',type:'Logistik',name:'Hub Westpark',size:83000,commit:83000,risk:3,duration:36,rate:0.125,description:'Logistikzentrum mit mittelfristigen Verträgen.',benefit:'Mietsteigerung durch Modernisierung',downside:'Leerstand und Refinanzierung'},
 {id:'re3',class:'Real Estate',type:'Büro Value Add',name:'Kranhaus Campus',size:49000,commit:49000,risk:4,duration:30,rate:0.16,description:'Bürogebäude mit Umbau- und Neuvermietungspotenzial.',benefit:'Wertsteigerung durch Sanierung',downside:'Hoher Leerstand bei schwacher Konjunktur'}
];
export const ROLES=[
 {id:'equity',name:'Aktienanalyst',salary:2800,fee:5500,description:'Fundamentaldaten und günstigere Börsenorders'},
 {id:'private',name:'Private-Markets-Analyst',salary:3400,fee:7500,description:'Günstigere Due Diligence und Risikoanalyse'},
 {id:'manager',name:'Investmentmanager',salary:4600,fee:10000,description:'Bessere Deal-Betreuung, Fondsfreischaltung'},
 {id:'ir',name:'Investor Relations',salary:3900,fee:8500,description:'Mehr Anlegerzusagen für eigene Fonds'}
];
export const CLASSES=['Private Equity','Private Debt','Infrastruktur','Real Estate'];
export const SECTORS=['Technologie','Industrie','Konsum','Energie'];