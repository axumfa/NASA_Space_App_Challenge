# Uzbek text for native-speaker review

All Uzbek text (Latin script) was written by the AI assistant and has **not** been checked by a native speaker. Please correct anything that is wrong, unnatural, or not the term farmers actually use. Placeholders in `{braces}` (numbers, crop names) must stay exactly as they are. Dataset and product names (NASA POWER, MODIS, SMAP, SoilGrids, FAO) are intentionally not translated.

To change a string, edit `src/fieldshift/i18n.py` (key shown below); `scripts/uzbek_review.py` regenerates this file.


## 1. Strings I am unsure about (65)

| key | English | Uzbek | why unsure |
|---|---|---|---|
| `ap.cover` | ground cover | tuproqni qoplash | parameter names in the 'approximate' list |
| `ap.drought_tol` | drought tolerance | qurg'oqchilikka chidamlilik | parameter names in the 'approximate' list |
| `ap.forage` | forage value | em-xashak qiymati | parameter names in the 'approximate' list |
| `ap.frost_kill_c` | frost-kill temperature | sovuq o'ldiruvchi harorat | parameter names in the 'approximate' list |
| `ap.gdd_req` | growing degree days needed | kerakli samarali harorat yig'indisi (GDD) | parameter names in the 'approximate' list |
| `ap.heat_thr_c` | heat threshold | issiqlik chegarasi | parameter names in the 'approximate' list |
| `ap.income` | income index | daromad ko'rsatkichi | parameter names in the 'approximate' list |
| `ap.ky` | yield response (Ky) | hosildorlikning suvga sezgirligi (Ky) | parameter names in the 'approximate' list |
| `ap.n_credit` | nitrogen credit | azot hissasi | parameter names in the 'approximate' list |
| `ap.om` | organic matter input | organik modda qo'shilishi | parameter names in the 'approximate' list |
| `ap.salinity_tol` | salt tolerance | tuzga chidamlilik | parameter names in the 'approximate' list |
| `ap.stages` | stage lengths | rivojlanish bosqichlari uzunligi | parameter names in the 'approximate' list |
| `ap.t_opt` | optimal temperature | optimal harorat | parameter names in the 'approximate' list |
| `ap.water_need_mm` | seasonal water need | mavsumiy suv ehtiyoji | parameter names in the 'approximate' list |
| `ex.gaps` | Information gaps | Ma'lumot bo'shliqlari | 'bo'shliqlar' for information gaps |
| `f.ndvi_green` |  Even at its lowest, the typical satellite greenness stays at **{low:.2f}** (bare soil is below {thr:.1f}). A 250 m pixel can stay green after harvest because of a second crop, stubble, weeds or mixed fields; check locally. |  Eng past nuqtada ham odatdagi sun'iy yo'ldosh yashilligi **{low:.2f}** darajasida qoladi (ochiq tuproq {thr:.1f} dan past). 250 m piksel hosildan keyin ikkinchi ekin, o'simlik qoldiqlari, begona o'tlar yoki aralash dalalar tufayli yashil qolishi mumkin; joyida tekshiring. | 'o'simlik qoldiqlari' for stubble (crop residue); a local word such as 'poxol' may be better |
| `f.trend` | **Trend {y0}–{y1}:** temperature {dt:+.2f} °C per decade ({tclear} trend); rain {dp:+.0f} mm per decade ({pclear} trend). | **Yo'nalish {y0}–{y1}:** harorat o'n yilda {dt:+.2f} °C ({tclear}); yog'in o'n yilda {dp:+.0f} mm ({pclear}). | 'trend' as 'yo'nalish' |
| `field.kansas` | Central Kansas, USA | Markaziy Kanzas, AQSH | 'Kanzas' spelling; 'AQSH' for USA |
| `g.contracts` | This tool compares crops on climate, soil and economics only. It does not know about any contracts, agreements or obligations you may have about what to plant, so some options may not be available to you. Check before you change a rotation. | Bu vosita ekinlarni faqat iqlim, tuproq va iqtisodiyot bo'yicha solishtiradi. U nima ekish bo'yicha sizdagi shartnomalar, kelishuvlar yoki majburiyatlardan xabardor emas, shuning uchun ayrim variantlar siz uchun mavjud bo'lmasligi mumkin. Almashlab ekishni o'zgartirishdan oldin tekshiring. | 'majburiyatlar' (obligations) and 'kelishuvlar' (agreements) are near-synonyms in this context; check the register |
| `g.rice` | Rice is a common crop in Karakalpakstan and is not modelled (it is not in the crop list), so rotations that include rice cannot be compared here. | Qoraqalpog'istonda sholi keng tarqalgan ekin, lekin u modellashtirilmagan (ekinlar ro'yxatida yo'q), shuning uchun sholi kiritilgan almashlab ekishlarni bu yerda solishtirib bo'lmaydi. | 'Qoraqalpog'iston' spelling; 'sholi' for rice |
| `g.versus_text` | • Climate values come from a ~50 km model/satellite blend, not from a weather station at your field. Over irrigated land it tends to run hotter and drier than the ground.<br>• Irrigation need and ET0 are computed (FAO-56 Penman–Monteith), not measured.<br>• Crop values (water use, heat limits, nitrogen credit) are regional approximations; check them with local advisers.<br>• Water supply from rivers or canals is not observed; use the irrigation-water slider to test shortages. | • Iqlim qiymatlari dalangizdagi ob-havo stansiyasidan emas, ~50 km li model/sun'iy yo'ldosh aralashmasidan olingan. Sug'oriladigan yerlarda u haqiqatdagidan issiqroq va quruqroq chiqishga moyil.<br>• Sug'orish ehtiyoji va ET0 o'lchanmagan, hisoblangan (FAO-56 Penman–Monteith).<br>• Ekin qiymatlari (suv sarfi, issiqlik chegaralari, azot hisobi) mintaqaviy taxminlar; mahalliy maslahatchilar bilan tekshiring.<br>• Daryo yoki kanallardan suv yetkazib berish hisobga olinmaydi; suv yetishmasligini sinash uchun sug'orish suvi slayderidan foydalaning. | technical bullets: check terms |
| `gl.dnw.d` | Years sorted into thirds by how much irrigation water crops needed: dry = highest need. | Yillar ekinlar qancha sug'orish suvi talab qilganiga qarab uchga bo'lingan: qurg'oqchil = eng ko'p talab. | technical explanation: check wording and terms |
| `gl.dnw.t` | Dry / normal / wet year | Qurg'oqchil / me'yoriy / seryog'in yil | technical term: check the established Uzbek term |
| `gl.et0.d` | Water that leaves the field as vapour: from the soil and through plant leaves. ET0 is how much a well-watered reference grass would lose on a given day. Crops use a share of it (the 'crop coefficient', Kc). | Dalani bug' sifatida tark etadigan suv: tuproqdan va o'simlik barglari orqali. ET0 — yaxshi sug'orilgan etalon o'tloq bir kunda qancha suv yo'qotishi. Ekinlar uning bir qismini ishlatadi («ekin koeffitsienti», Kc). | technical explanation: check wording and terms |
| `gl.et0.t` | Evapotranspiration (ET0) | Evapotranspiratsiya (ET0) | technical term: check the established Uzbek term |
| `gl.fit.d` | A relative 0–100 comparison among the options shown, based on the sliders. It changes when you change the options or sliders. | Ko'rsatilgan variantlar orasida slayderlarga asoslangan nisbiy 0–100 solishtirish. Variantlar yoki slayderlarni o'zgartirsangiz, u ham o'zgaradi. | technical explanation: check wording and terms |
| `gl.fit.t` | Fit to your priorities | Ustuvorliklarga moslik | technical term: check the established Uzbek term |
| `gl.frost.d` | Chance that the night minimum drops to 0 °C or lower. Late spring and early autumn frosts can kill young or ripening crops. | Tungi eng past harorat 0 °C yoki undan pastga tushish ehtimoli. Kech bahorgi va erta kuzgi qirov yosh yoki pishayotgan ekinlarni nobud qilishi mumkin. | technical explanation: check wording and terms |
| `gl.frost.t` | Frost risk | Qirov xavfi | technical term: check the established Uzbek term |
| `gl.gdd.d` | A running total of useful warmth. A crop needs a certain amount to reach maturity. | Foydali issiqlikning to'planib boruvchi yig'indisi. Ekin pishishi uchun ma'lum miqdor kerak. | technical explanation: check wording and terms |
| `gl.gdd.t` | Growing degree days | Samarali harorat yig'indisi (GDD) | technical term: check the established Uzbek term |
| `gl.heat.d` | Days when the daytime high goes above a crop's tolerance (for example 35–38 °C). Flowers and grain can fail. | Kunduzgi eng yuqori harorat ekin chidamidan oshgan kunlar (masalan, 35–38 °C). Gullar va don ziyon ko'rishi mumkin. | technical explanation: check wording and terms |
| `gl.heat.t` | Heat stress | Issiqdan zo'riqish | technical term: check the established Uzbek term |
| `gl.irr.d` | Crop water use over the season minus the rain that actually reaches the roots. Shown in mm; 100 mm = 1,000 m³ per hectare. | Mavsum davomida ekinning suv sarfi minus ildizga haqiqatan yetib boradigan yog'in. mm da ko'rsatiladi; 100 mm = gektariga 1000 m³. | technical explanation: check wording and terms |
| `gl.irr.t` | Irrigation need | Sug'orish ehtiyoji | technical term: check the established Uzbek term |
| `gl.ndvi.d` | A 'greenness' number from satellites (0 = bare, 0.8 = dense crop). Low values show when the field is bare. | Sun'iy yo'ldoshlardan olinadigan «yashillik» ko'rsatkichi (0 = ochiq tuproq, 0,8 = zich ekin). Past qiymatlar dala ochiq bo'lgan vaqtni ko'rsatadi. | technical explanation: check wording and terms |
| `gl.ndvi.t` | NDVI | NDVI | technical term: check the established Uzbek term |
| `gl.sma.d` | How much wetter or drier the soil is than normal for the time of year. Negative = drier than usual. | Tuproq yilning shu vaqti uchun odatdagidan qancha nam yoki quruq ekanligi. Manfiy = odatdagidan quruqroq. | technical explanation: check wording and terms |
| `gl.sma.t` | Soil-moisture anomaly | Tuproq namligi anomaliyasi | technical term: check the established Uzbek term |
| `gl.wb.d` | Rain minus ET0 for a month. Negative means the air can take more water than rain provides, so plants need irrigation or stored soil water. | Oy uchun yog'in minus ET0. Manfiy qiymat havo yog'indan ko'proq suv olishi mumkinligini bildiradi, shuning uchun o'simliklarga sug'orish yoki tuproqdagi zaxira suv kerak. | technical explanation: check wording and terms |
| `gl.wb.t` | Water balance | Suv balansi | technical term: check the established Uzbek term |
| `gl.yar.d` | How much of a normal harvest may be lost because the crop gets less water than it needs (FAO yield-response factors). It is 0 when irrigation water is plentiful. Heat is shown separately, as a count of very hot days. | Ekin kerakli suvdan kamroq olgani sababli oddiy hosilning qancha qismi yo'qolishi mumkin (FAO hosil-javob koeffitsientlari). Sug'orish suvi yetarli bo'lsa, 0 bo'ladi. Issiqlik alohida — juda issiq kunlar soni sifatida ko'rsatiladi. | technical explanation: check wording and terms |
| `gl.yar.t` | Yield at risk | Hosil xavfi | technical term: check the established Uzbek term |
| `m.lastfrost` | Last spring frost | Oxirgi bahorgi qirov | 'qirov' for frost |
| `o.yield_low` | At full irrigation supply there is almost no water-shortage risk. Lower the irrigation supply in "{sec}" to see where each option breaks. | To'liq sug'orish ta'minotida suv yetishmasligi xavfi deyarli yo'q. Har bir variant qayerda buzilishini ko'rish uchun "{sec}" bo'limida sug'orish ta'minotini kamaytiring. | uses the sidebar section name (ui.sidebar_what) so the wording always matches |
| `p.forage` | Forage value | Em-xashak qiymati | 'em-xashak' vs 'ozuqa' for forage |
| `p.nitrogen` | Nitrogen fixing | Azot to'plash | 'azot to'plash' vs 'azot biriktirish' for nitrogen fixing |
| `p.soil_om` | Soil organic matter | Tuproqdagi organik moddalar (chirindi) | 'chirindi' (humus) vs 'organik moddalar' |
| `side.whatif` | What if…? | Agar shunday bo'lsa…? | natural phrasing of 'What if…?' |
| `soil.bdod_kg_dm3` | bulk density kg/dm³ | hajmiy zichlik kg/dm³ | 'hajmiy zichlik' for bulk density |
| `soil.clay_pct` | clay % | gil % | soil texture terms: gil/qum/chang |
| `soil.tex.clay` | clay | gil | soil texture class names (USDA-style) in Uzbek: gil / qumloq / qumoq / changli qumoq / gilli qumoq |
| `soil.tex.clay_loam` | clay loam | gilli qumoq | 'clay loam': 'gilli qumoq' |
| `soil.tex.loam` | loam | qumoq | 'loam': 'qumoq' (Uzbek soil science uses light/medium/heavy qumoq) |
| `soil.tex.sandy` | sandy | qumloq | 'sandy' (sand >= 70%): 'qumloq' |
| `soil.tex.silty` | silty loam | changli qumoq | 'silty (loam)': 'changli qumoq' |
| `soil.texture` | texture | tuproq turi | texture class names are not translated |
| `sum.tradeoff` | **Main trade-off:** {tradeoff}. | **Asosiy kamchilik:** {tradeoff}. | 'trade-off' rendered as 'kamchilik' (drawback) |
| `ui.elev` | ~50 km cell average elevation: {m:.0f} m | ~50 km katakning o'rtacha balandligi: {m:.0f} m | phrasing of the average elevation of the climate grid cell |
| `ui.grp_env` | Environment | Atrof-muhit | 'Atrof-muhit' for environment |
| `ui.hemi_e` | E | Shq | compass abbreviations Sh (north), Shq (east), J (south), G' (west) |
| `ui.kpi_et0` | Reference ET0 | Namlanish talabi (ET0) | 'namlanish talabi' for ET0 |
| `ui.sidebar_what` | Test a scenario | Stsenariyni sinab ko'ring | 'Stsenariy' for scenario |
| `ui.tagline` | Crop-rotation decision support | Almashlab ekish qaror vositasi | short for 'decision support': 'qaror vositasi' (decision tool); shortened so it fits one line |
| `viz.fit_title` | {short} by type of year (bars = typical, whiskers = 10th–90th percentile) | {short}, yil turi bo'yicha (ustun = odatdagi, chiziq = 10–90-protsentil) | 'protsentil' |

## 2. Crop names

| crop | English | Uzbek | note |
|---|---|---|---|
| `cotton` | Cotton | Paxta |  |
| `winter_wheat` | Winter wheat | Kuzgi bug'doy |  |
| `barley` | Winter barley | Kuzgi arpa |  |
| `maize` | Maize (grain) | Makkajo'xori (don uchun) |  |
| `sorghum` | Sorghum | Jo'xori (sorgo) | check sorghum vs jo'xori usage |
| `millet` | Millet | Tariq |  |
| `alfalfa` | Alfalfa (1 yr stand modelled) | Beda (1 yillik ekin sifatida modellashtirilgan) |  |
| `mung_bean` | Mung bean | Mosh |  |
| `chickpea` | Chickpea (spring sown) | No'xat (bahorda ekiladi) |  |
| `lentil` | Lentil (spring sown) | Yasmiq (bahorda ekiladi) |  |
| `soybean` | Soybean | Soya |  |
| `sunflower` | Sunflower | Kungaboqar |  |
| `safflower` | Safflower | Aspir | safflower: 'aspir' vs another local name |
| `rapeseed` | Winter rapeseed | Kuzgi raps | rapeseed: 'raps' vs 'kolza' |
| `rye_cover` | Winter rye cover crop | Kuzgi javdar (qoplama ekin) | 'qoplama ekin' for cover crop; 'siderat' also used |
| `hairy_vetch` | Hairy vetch cover crop | Tukli vika (qoplama ekin) | 'tukli vika' for hairy vetch |
| `clover` | Berseem/crimson clover cover | Sebarga / berseem (qoplama ekin) | clover vs berseem clover naming |
| `potato` | Potato | Kartoshka |  |
| `melon` | Melon | Qovun |  |
| `sugar_beet` | Sugar beet | Qand lavlagi |  |

## 3. All other strings (421), please still skim

| key | English | Uzbek |
|---|---|---|
| `app.subtitle` | Explore crop-rotation options for your field using NASA satellite and climate data. | NASA sun'iy yo'ldosh va iqlim ma'lumotlari yordamida dalangiz uchun ekin almashlab ekish variantlarini ko'rib chiqing. |
| `app.disclaimer` | <b>This tool supports, and does not replace, your own judgment and that of a local agronomist.</b> Results are estimates from regional data; check them with local experts before changing what you grow. | <b>Bu vosita sizning va mahalliy agronomning fikrini qo'llab-quvvatlaydi, uning o'rnini bosmaydi.</b> Natijalar mintaqaviy ma'lumotlarga asoslangan taxminlar; nima ekishni o'zgartirishdan oldin mahalliy mutaxassislar bilan tekshiring. |
| `lang.label` | Language | Til |
| `side.field` | Your field | Sizning dalangiz |
| `side.choose` | Choose a field | Dalani tanlang |
| `side.own` | My own location | O'z joylashuvim |
| `side.lat` | Latitude | Kenglik |
| `side.lon` | Longitude | Uzunlik |
| `side.grow` | What you grow now | Hozir nima ekasiz |
| `side.grow_help` | Crops in the order you grow them (one per season/year). | Ekinlarni ekish tartibida kiriting (har bir mavsum/yil uchun bittadan). |
| `side.crop` | Crop {n} | {n}-ekin |
| `side.crop_opt` | Crop {n} (optional) | {n}-ekin (ixtiyoriy) |
| `side.none` | — none — | — yo'q — |
| `side.matters` | What matters to you | Siz uchun nima muhim |
| `side.quick` | Quick settings | Tezkor sozlamalar |
| `side.quick_help` | Pre-sets the sliders; you can still change them. | Slayderlarni oldindan sozlaydi; keyin o'zgartirishingiz mumkin. |
| `profile.Balanced` | Balanced | Muvozanatli |
| `profile.water-first` | Water first | Avval suv tejash |
| `profile.income-first` | Income first | Avval daromad |
| `profile.soil-first` | Soil first | Avval tuproq |
| `p.water_saving` | Water saving | Suv tejash |
| `p.erosion` | Erosion reduction | Eroziyani kamaytirish |
| `p.income` | Market / income | Bozor / daromad |
| `pshort.water_saving` | Water | Suv |
| `pshort.soil_om` | Soil humus | Chirindi |
| `pshort.nitrogen` | Nitrogen | Azot |
| `pshort.erosion` | Erosion | Eroziya |
| `pshort.forage` | Forage | Em-xashak |
| `pshort.income` | Income | Daromad |
| `ph.water_saving` | Needing less irrigation water. | Sug'orish suvi kamroq kerak bo'lishi. |
| `ph.soil_om` | Building organic matter (soil 'humus') that holds water and nutrients. | Suv va oziq moddalarni ushlab turuvchi organik moddalar (tuproq «chirindisi»)ni to'plash. |
| `ph.nitrogen` | Legumes put nitrogen into the soil, saving fertiliser. | Dukkakli ekinlar tuproqqa azot qo'shadi, o'g'it tejaladi. |
| `ph.erosion` | Keeping the soil covered so wind and rain do not carry it away. | Tuproqni yopiq saqlash, shamol va yomg'ir uni olib ketmasligi uchun. |
| `ph.forage` | Feed for animals (hay, grazing). | Chorva uchun ozuqa (pichan, o'tlatish). |
| `ph.income` | Expected market income from the crops. | Ekinlardan kutilayotgan bozor daromadi. |
| `side.rain` | Rainfall change (%) | Yog'ingarchilik o'zgarishi (%) |
| `side.rain_help` | Applied to every day of the climate record. | Iqlim yozuvidagi har bir kunga qo'llanadi. |
| `side.temp` | Temperature rise (°C) | Harorat ko'tarilishi (°C) |
| `side.supply` | Irrigation water available (% of what crops need) | Mavjud sug'orish suvi (ekinlar ehtiyojining %) |
| `side.supply_help` | 100% = enough water in almost every year. Lower values show how much yield is put at risk by a shortage. | 100% = deyarli har yili suv yetarli. Past qiymatlar suv yetishmasligi hosilni qanchalik xavf ostiga qo'yishini ko'rsatadi. |
| `side.apply` | Apply what-if | Qo'llash |
| `err.pick` | Pick at least one crop you grow now. | Hozir ekadigan kamida bitta ekinni tanlang. |
| `err.dup` | The same crop is listed twice; each crop should appear once in your rotation. | Bir xil ekin ikki marta kiritilgan; har bir ekin almashlab ekishda bir marta bo'lishi kerak. |
| `err.cal` | This crop order does not fit a repeating calendar of 1–3 years (the crops overlap in time or the cycle is too long). Try another order. | Bu ekin tartibi 1–3 yillik takrorlanuvchi taqvimga sig'maydi (ekinlar vaqt bo'yicha ustma-ust tushadi yoki sikl juda uzun). Boshqa tartibni sinab ko'ring. |
| `err.power` | Could not get NASA POWER climate data for this place ({e}). Check your connection; demo fields work offline once downloaded. | Bu joy uchun NASA POWER iqlim ma'lumotlarini olib bo'lmadi ({e}). Ulanishni tekshiring; namunaviy dalalar yuklab olingandan keyin internetsiz ishlaydi. |
| `spin.climate` | Getting NASA climate data for this field… | Bu dala uchun NASA iqlim ma'lumotlari olinmoqda… |
| `spin.pool` | Comparing rotation options… | Almashlab ekish variantlari solishtirilmoqda… |
| `whatif.active` | What-if active: rainfall {rain:+d}%, temperature +{temp:.1f} °C, irrigation water {supply:.0f}%. | «Agar shunday bo'lsa» rejimi yoqilgan: yog'ingarchilik {rain:+d}%, harorat +{temp:.1f} °C, sug'orish suvi {supply:.0f}%. |
| `view.field` | Your field | Sizning dalangiz |
| `view.options` | Rotation options | Almashlab ekish variantlari |
| `view.glossary` | Glossary & data | Lug'at va ma'lumotlar |
| `field.fergana` | Fergana Valley, Uzbekistan | Farg'ona vodiysi, O'zbekiston |
| `field.karakalpakstan` | Karakalpakstan farmland (near Nukus), Uzbekistan | Qoraqalpog'iston ekin maydoni (Nukus yaqinida), O'zbekiston |
| `field.bukhara` | Bukhara region farmland, Uzbekistan | Buxoro viloyati ekin maydoni, O'zbekiston |
| `field.samarkand` | Samarkand region farmland, Uzbekistan | Samarqand viloyati ekin maydoni, O'zbekiston |
| `f.where` | Where is your field? | Dalangiz qayerda? |
| `f.marker` | Your field | Sizning dalangiz |
| `f.mapcap` | Click the map to move the field. Climate data is for a ~50 km area around the point. | Dalani ko'chirish uchun xaritani bosing. Iqlim ma'lumotlari nuqta atrofidagi ~50 km hudud uchun. |
| `f.keynums` | Key numbers (typical year) | Asosiy ko'rsatkichlar (odatdagi yil) |
| `m.rain` | Rain per year | Yillik yog'in |
| `m.et0` | Water the air can take (ET0) | Havo oladigan suv (ET0) |
| `m.et0_help` | Evapotranspiration: water lost from soil and plants to the air. | Evapotranspiratsiya: tuproq va o'simliklardan havoga yo'qoladigan suv. |
| `m.firstfrost` | First autumn frost | Birinchi kuzgi qirov |
| `m.frostdays` | Frost days per year | Yiliga qirovli kunlar |
| `m.hotdays` | Very hot days (≥ 35 °C) | Juda issiq kunlar (≥ 35 °C) |
| `f.clear` | clear | aniq yo'nalish |
| `f.notclear` | not clear | aniq yo'nalish yo'q |
| `f.bare_h` | Bare soil and vulnerable seasons for what you grow now | Hozir ekadigan ekinlaringiz uchun ochiq tuproq va zaif mavsumlar |
| `f.bare_text` | Your field is bare about **{days:.0f} days a year** according to the crop calendar{wins}. | Ekin taqvimiga ko'ra dalangiz yiliga taxminan **{days:.0f} kun** ochiq qoladi{wins}. |
| `f.bare_win` | {start} for {n} days | {start} dan {n} kun |
| `f.ndvi_text` | Satellite view: on days with a clear observation, the field is below the bare-soil greenness level about **{obs:.0f} days a year** (the crop calendar above says {cal:.0f}). | Sun'iy yo'ldosh ma'lumoti: aniq kuzatuv bo'lgan kunlarda dala yiliga taxminan **{obs:.0f} kun** ochiq tuproq yashillik darajasidan past (yuqoridagi ekin taqvimi bo'yicha {cal:.0f}). |
| `f.ndvi_diff` |  Differences usually mean sowing dates, weeds or cloud gaps differ from the typical calendar. |  Farq odatda ekish sanalari, begona o'tlar yoki bulutli kunlar odatdagi taqvimdan farq qilishini bildiradi. |
| `f.ndvi_unobs` |  About **{unobs:.0f} days a year** ({months}) have no clear observation (snow or cloud), so the satellite cannot confirm the bare period then. |  Yiliga taxminan **{unobs:.0f} kun** ({months}) aniq kuzatuv yo'q (qor yoki bulut), shuning uchun sun'iy yo'ldosh o'sha paytdagi ochiq davrni tasdiqlay olmaydi. |
| `f.ndvi_missing` | Satellite vegetation (MODIS NDVI) is not loaded for this field, so bare periods come from typical sowing and harvest dates, not from observed greenness. Put the AppEEARS CSV in data/raw/ to add it. | Bu dala uchun sun'iy yo'ldosh o'simlik ma'lumoti (MODIS NDVI) yuklanmagan, shuning uchun ochiq davrlar kuzatilgan yashillikdan emas, odatdagi ekish va yig'im-terim sanalaridan olingan. Qo'shish uchun AppEEARS CSV faylini data/raw/ papkasiga joylang. |
| `f.smap_missing` | Satellite soil moisture (SMAP) is not usable for this field, so this is NASA POWER's model estimate of root-zone wetness (~50 km grid), not a satellite measurement. See the information gaps for the reason. | Bu dala uchun sun'iy yo'ldosh tuproq namligi (SMAP) yaroqli emas, shuning uchun bu NASA POWER'ning ildiz qatlami namligi bo'yicha model baholashi (~50 km katak), sun'iy yo'ldosh o'lchovi emas. Sababi ma'lumot bo'shliqlarida ko'rsatilgan. |
| `f.vuln` | **When your current crops are most vulnerable** (typical year, from the daily weather record): | **Hozirgi ekinlaringiz qachon eng zaif** (odatdagi yil, kunlik ob-havo yozuvidan): |
| `col.crop` | Crop | Ekin |
| `col.frost` | Frost days in season | Mavsumdagi qirovli kunlar |
| `col.hot` | Hot days (≥ {thr} °C) | Issiq kunlar (≥ {thr} °C) |
| `col.irr` | Water to add by irrigation (mm) | Sug'orish bilan qo'shiladigan suv (mm) |
| `col.fit` | Climate fit (0-100) | Iqlimga moslik (0–100) |
| `f.soil` | Soil | Tuproq |
| `f.soil_na` | Soil data is not available for this field yet (SoilGrids could not be reached and no manual reading was found). It is listed as an information gap and is not used in the scores. | Bu dala uchun tuproq ma'lumoti hozircha mavjud emas (SoilGrids'ga ulanib bo'lmadi va qo'lda kiritilgan qiymat topilmadi). U ma'lumot bo'shliqlari ro'yxatida ko'rsatilgan va ballarda ishlatilmaydi. |
| `soil.sand_pct` | sand % | qum % |
| `soil.silt_pct` | silt % | chang (silt) % |
| `soil.soc_g_kg` | organic carbon g/kg | organik uglerod g/kg |
| `soil.phh2o` | pH | pH |
| `f.gaps` | What data is missing for this field? | Bu dala uchun qanday ma'lumotlar yetishmayapti? |
| `fit.label` | Fit to your priorities (compared among these options) | Ustuvorliklaringizga moslik (shu variantlar orasida solishtirilgan) |
| `fit.short` | Fit to your priorities | Ustuvorliklarga moslik |
| `o.caption` | A relative score from 0 to 100 that compares the options shown here, using the priorities you set. It is not a grade or a yield forecast. Real units (mm of water, days, % yield at risk) are shown on every card. | Siz belgilagan ustuvorliklar asosida bu yerda ko'rsatilgan variantlarni solishtiradigan 0 dan 100 gacha nisbiy ball. Bu baho yoki hosil bashorati emas. Haqiqiy birliklar (suv mm, kunlar, hosil xavfi %) har bir kartochkada ko'rsatilgan. |
| `o.ties` | These options do not differ meaningfully on: {list}. That priority does not change the ranking. | Bu variantlar quyidagi bo'yicha sezilarli farq qilmaydi: {list}. Bu ustuvorlik tartibni o'zgartirmaydi. |
| `o.current` | Your current rotation | Hozirgi almashlab ekishingiz |
| `o.fit_cap` | {short} · typical range {lo:.0f}–{hi:.0f} · dry {d:.0f} / normal {n:.0f} / wet {w:.0f} | {short} · odatdagi oraliq {lo:.0f}–{hi:.0f} · qurg'oqchil {d:.0f} / me'yoriy {n:.0f} / seryog'in {w:.0f} |
| `o.irr` | Irrigation need: <b>{irr:.0f} mm/yr</b>{pct} | Sug'orish ehtiyoji: <b>{irr:.0f} mm/yil</b>{pct} |
| `o.vs_now` |  ({pct:+.0f}% vs now) |  (hozirgiga nisbatan {pct:+.0f}%) |
| `o.bare` | Bare soil: <b>{d:.0f} days/yr</b> | Ochiq tuproq: <b>yiliga {d:.0f} kun</b> |
| `o.nitrogen` | Nitrogen from legumes: <b>{n:.0f} kg N/ha/yr</b> | Dukkakli ekinlardan azot: <b>yiliga {n:.0f} kg N/ga</b> |
| `o.yield` | Yield at risk from water shortage: <b>{m:.0f}%</b> typical, <b>{p:.0f}%</b> in a bad year (1 in 10) | Suv yetishmasligidan hosil xavfi: odatda <b>{m:.0f}%</b>, yomon yilda (10 yilda 1) <b>{p:.0f}%</b> |
| `o.heat` | {crop}: <b>{n:.0f}</b> days above {thr:.0f} °C in season (bad year: {p:.0f}) | {crop}: mavsumda {thr:.0f} °C dan yuqori <b>{n:.0f}</b> kun (yomon yilda: {p:.0f}) |
| `o.heat_cap` | Heat exposure is a count of hot days, not a yield forecast. Temperatures come from ~50 km reanalysis that runs hot over irrigated land. | Issiqlik ta'siri — issiq kunlar soni, hosil bashorati emas. Haroratlar ~50 km li qayta tahlildan olingan va sug'oriladigan yerlarda issiqroq chiqadi. |
| `o.radar_cap` | Shaded radar = this option, dotted = your current rotation. Each axis compares options with each other (outer edge = best of those shown). | Bo'yalgan radar = shu variant, nuqtali = hozirgi almashlab ekishingiz. Har bir o'q variantlarni bir-biri bilan solishtiradi (tashqi chekka = ko'rsatilganlar ichida eng yaxshisi). |
| `ex.why` | Why this option | Nima uchun bu variant |
| `ex.evidence` | Evidence (numbers) | Dalillar (raqamlar) |
| `ex.benefits` | Benefits | Afzalliklar |
| `ex.tradeoff` | Trade-off: {t} | Kamchilik: {t} |
| `ex.risks` | Risks to check with a local expert | Mahalliy mutaxassis bilan tekshiriladigan xavflar |
| `rule.legume` | Adds a nitrogen-fixing crop: {crop} | Azot to'plovchi ekin qo'shiladi: {crop} |
| `rule.cover` | Adds a cover crop in a bare window: {crop} | Ochiq davrga qoplama ekin qo'shiladi: {crop} |
| `rule.swap_drought` | Replaces {old} with the more drought-tolerant {crop} | {old} o'rniga qurg'oqchilikka chidamliroq {crop} ekiladi |
| `rule.income` | Replaces {old} with the higher-value {crop} | {old} o'rniga daromadliroq {crop} ekiladi |
| `rule.perennial` | Adds a deep-rooted perennial: {crop} | Chuqur ildizli ko'p yillik ekin qo'shiladi: {crop} |
| `rule.winter_crop` | Adds a winter crop to break the cycle: {crop} | Siklni buzish uchun kuzgi ekin qo'shiladi: {crop} |
| `rule.pinned` | Added as a comparison option: {crop} | Solishtirish uchun variant sifatida qo'shilgan: {crop} |
| `g.title` | What the words mean | So'zlar nimani anglatadi |
| `g.data` | NASA and other data used | Foydalanilgan NASA va boshqa ma'lumotlar |
| `g.col_source` | Source | Manba |
| `g.col_for` | What for | Nima uchun |
| `g.col_res` | Resolution | Aniqlik |
| `g.col_period` | Period | Davr |
| `g.col_status` | Status | Holati |
| `g.power_for` | Daily temperature, rain, humidity, wind, sunshine, soil wetness | Kunlik harorat, yog'in, namlik, shamol, quyosh nuri, tuproq namligi |
| `g.power_res` | ~50 km grid, daily | ~50 km katak, kunlik |
| `g.used` | Used | Ishlatilgan |
| `g.soil_for` | Soil texture, organic carbon, pH | Tuproq turi, organik uglerod, pH |
| `g.soil_status` | Used only if reachable or entered by hand | Faqat mavjud bo'lsa yoki qo'lda kiritilsa ishlatiladi |
| `g.static` | static | o'zgarmas |
| `g.ndvi_for` | Greenness, bare-soil periods | Yashillik, ochiq tuproq davrlari |
| `g.res_ndvi` | 250 m, 16-day | 250 m, 16 kunlik |
| `g.ndvi_used` | Used for display and comparison | Ko'rsatish va solishtirish uchun ishlatilgan |
| `g.ndvi_not` | Not loaded for this field | Bu dala uchun yuklanmagan |
| `g.smap_for` | Soil moisture anomaly | Tuproq namligi anomaliyasi |
| `g.smap_used` | Used for display | Ko'rsatish uchun ishlatilgan |
| `g.smap_not` | Not loaded; POWER soil wetness is the model-based stand-in | Yuklanmagan; o'rniga POWER tuproq namligi (model asosida) ishlatiladi |
| `g.other_for` | Rain cross-check; slope | Yog'inni tekshirish; qiyalik |
| `g.not_yet` | Not yet loaded | Hozircha yuklanmagan |
| `g.versus` | Satellite and model data versus your ground | Sun'iy yo'ldosh va model ma'lumotlari va sizning yeringiz |
| `footer` | Decision support only. Validate with local agronomists. Data: NASA POWER, ISRIC SoilGrids. Method notes: docs/methodology.md. | Faqat qaror qabul qilishga yordam. Mahalliy agronomlar bilan tasdiqlang. Ma'lumotlar: NASA POWER, ISRIC SoilGrids. Usul izohlari: docs/methodology.md. |
| `viz.wb_title` | Rain vs. water demand, average month | Yog'in va suv talabi, o'rtacha oy |
| `viz.wb_y` | mm per month | mm/oy |
| `viz.wb_rain` | Rain (mm) | Yog'in (mm) |
| `viz.wb_et0` | Water the air can take (ET0, mm) | Havo oladigan suv (ET0, mm) |
| `viz.frost_title` | Chance of a frost (≤ 0 °C) in each week, share of years | Har bir haftada qirov (≤ 0 °C) bo'lish ehtimoli, yillar ulushi |
| `viz.heat_title` | Hot days (max ≥ {thr:.0f} °C) per month, average year | Oyiga issiq kunlar (eng yuqori ≥ {thr:.0f} °C), o'rtacha yil |
| `viz.week` | week of year | yil haftasi |
| `viz.pct_years` | % of years | yillar % |
| `viz.days` | days | kun |
| `viz.cal_title` | Crop calendar: green = crop in the field, red = bare soil | Ekin taqvimi: yashil = dalada ekin, qizil = ochiq tuproq |
| `viz.current` | Current | Hozirgi |
| `viz.this` | This option | Shu variant |
| `viz.dry` | Dry years (high water need) | Qurg'oqchil yillar (suv talabi yuqori) |
| `viz.normal` | Normal years | Me'yoriy yillar |
| `viz.wet` | Wet years (low water need) | Seryog'in yillar (suv talabi past) |
| `viz.rel` | relative score | nisbiy ball |
| `viz.ndvi_title` | Satellite greenness through the year (red = typically bare) | Yil davomida sun'iy yo'ldosh yashilligi (qizil = odatda ochiq) |
| `viz.ndvi_y` | NDVI (0 bare – 0.8 dense crop) | NDVI (0 ochiq – 0,8 zich ekin) |
| `viz.ndvi_spread` | typical spread (25–75%) | odatdagi tarqalish (25–75%) |
| `viz.ndvi_med` | greenness (NDVI), median year | yashillik (NDVI), o'rtacha yil |
| `viz.ndvi_line` | bare soil below this | bundan pasti ochiq tuproq |
| `viz.sm_title` | Satellite soil moisture: wetter (+) or drier (−) than normal, average by month | Sun'iy yo'ldosh tuproq namligi: odatdagidan nam (+) yoki quruq (−), oylar bo'yicha o'rtacha |
| `viz.sm_y` | z-score | z-ball |
| `viz.rw_title` | Root-zone soil wetness (NASA POWER model): 0 = dry, 1 = saturated | Ildiz qatlami tuproq namligi (NASA POWER modeli): 0 = quruq, 1 = to'yingan |
| `viz.rw_range` | typical range (10–90% of years) | odatdagi oraliq (yillarning 10–90%) |
| `viz.rw_med` | median year | o'rtacha yil |
| `viz.rw_y` | wetness | namlik |
| `sum.title` | In plain words | Oddiy so'zlar bilan |
| `sum.best` | **Best fit for your priorities:** {crops} (fit {fit:.0f}; your current rotation {cur:.0f}). | **Ustuvorliklaringizga eng mos variant:** {crops} (moslik {fit:.0f}; hozirgi almashlab ekishingiz {cur:.0f}). |
| `sum.best_is_current` | **Your current rotation fits your priorities best** among these options (fit {fit:.0f}; next best {other:.0f}). | **Hozirgi almashlab ekishingiz ustuvorliklaringizga eng mos keladi** (moslik {fit:.0f}; keyingisi {other:.0f}). |
| `sum.reason` | **Why:** {reasons}. | **Sababi:** {reasons}. |
| `sum.reason_none` | **Why:** it is ahead on the combination of your priorities, but by no single large margin. | **Sababi:** ustuvorliklaringiz yig'indisi bo'yicha oldinda, lekin birorta katta farq bilan emas. |
| `sum.tradeoff_none` | **Main trade-off:** none of your priorities gets clearly worse than in your current rotation. | **Asosiy kamchilik:** ustuvorliklaringizdan birortasi hozirgi almashlab ekishingizdagidan sezilarli yomonlashmaydi. |
| `sum.check` | **Check with a local agronomist:** {check} | **Mahalliy agronom bilan tekshiring:** {check} |
| `sum.caveat` | This summary is built only from the numbers on this page. It compares the options shown; it is not a forecast. | Bu xulosa faqat shu sahifadagi raqamlardan tuzilgan. U ko'rsatilgan variantlarni solishtiradi; bashorat emas. |
| `r.water` | irrigation need {new:.0f} mm/yr instead of {old:.0f} mm ({pct:+.0f}%) | sug'orish ehtiyoji {old:.0f} mm o'rniga {new:.0f} mm/yil ({pct:+.0f}%) |
| `r.nitrogen` | legumes add about {new:.0f} kg N/ha per year (now {old:.0f}) | dukkakli ekinlar yiliga taxminan {new:.0f} kg N/ga azot qo'shadi (hozir {old:.0f}) |
| `r.erosion` | bare soil falls to {new:.0f} days a year (now {old:.0f}) | ochiq tuproq yiliga {new:.0f} kungacha kamayadi (hozir {old:.0f}) |
| `r.soil_om` | more organic matter returns to the soil (index {new:.0f} vs {old:.0f} of 100) | tuproqqa ko'proq organik modda qaytadi (ko'rsatkich {new:.0f}, hozir {old:.0f}, 100 dan) |
| `r.forage` | more feed value (index {new:.0f} vs {old:.0f} of 100) | em-xashak qiymati yuqoriroq (ko'rsatkich {new:.0f}, hozir {old:.0f}, 100 dan) |
| `r.income` | higher expected market income (index {new:.0f} vs {old:.0f} of 100) | kutilayotgan bozor daromadi yuqoriroq (ko'rsatkich {new:.0f}, hozir {old:.0f}, 100 dan) |
| `t.water` | it needs more water: {new:.0f} mm/yr instead of {old:.0f} mm ({pct:+.0f}%) | suv ko'proq kerak: {old:.0f} mm o'rniga {new:.0f} mm/yil ({pct:+.0f}%) |
| `t.nitrogen` | less nitrogen from legumes ({new:.0f} kg N/ha per year instead of {old:.0f}) | dukkakli ekinlardan azot kamroq (yiliga {old:.0f} kg N/ga o'rniga {new:.0f}) |
| `t.erosion` | more bare soil ({new:.0f} days a year instead of {old:.0f}) | ochiq tuproq ko'proq (yiliga {old:.0f} kun o'rniga {new:.0f} kun) |
| `t.soil_om` | less organic matter returns to the soil (index {new:.0f} vs {old:.0f} of 100) | tuproqqa organik modda kamroq qaytadi (ko'rsatkich {new:.0f}, hozir {old:.0f}, 100 dan) |
| `t.forage` | less feed value (index {new:.0f} vs {old:.0f} of 100) | em-xashak qiymati pastroq (ko'rsatkich {new:.0f}, hozir {old:.0f}, 100 dan) |
| `t.income` | lower expected market income (index {new:.0f} vs {old:.0f} of 100) | kutilayotgan bozor daromadi pastroq (ko'rsatkich {new:.0f}, hozir {old:.0f}, 100 dan) |
| `t.shortage` | in a water-short year (1 in 10) yield at risk from shortage is {new:.0f}% instead of {old:.0f}% | suv taqchil yilda (10 yilda 1) suv yetishmasligidan hosil xavfi {old:.0f}% o'rniga {new:.0f}% |
| `c.salinity` | {crop} is sensitive to salt; check soil and irrigation-water salinity before sowing it. | {crop} tuzga sezgir; ekishdan oldin tuproq va sug'orish suvining sho'rligini tekshiring. |
| `c.newcrop` | {crop} is new for you; confirm seed, machinery and a buyer or market before committing. | {crop} siz uchun yangi; qaror qilishdan oldin urug', texnika va xaridor yoki bozorni aniqlang. |
| `c.water` | confirm that irrigation water will really be available ({irr:.0f} mm/yr is needed). | sug'orish suvi haqiqatan mavjud bo'lishini tasdiqlang (yiliga {irr:.0f} mm kerak). |
| `c.dates` | check that the sowing and harvest dates in this calendar fit your local weather and farm work. | bu taqvimdagi ekish va yig'im-terim sanalari mahalliy ob-havo va dala ishlariga mos kelishini tekshiring. |
| `c.cycle` | this rotation takes {years} years to complete; check that it fits your land and contracts. | bu almashlab ekish {years} yilda tugaydi; yeringiz va shartnomalaringizga mos kelishini tekshiring. |
| `g.soil` | Soil: not used in the scores (shown for information only; see the Soil section for its status). | Tuproq: ballarda ishlatilmaydi (faqat ma'lumot uchun ko'rsatiladi; holati uchun Tuproq bo'limiga qarang). |
| `g.ndvi_ok` | Satellite NDVI ({nv}/{nt} observations pass quality checks, {rng}) is shown and compared with the crop calendar; the scores still use the calendar. | Sun'iy yo'ldosh NDVI ({nv}/{nt} kuzatuv sifat tekshiruvidan o'tdi, {rng}) ko'rsatiladi va ekin taqvimi bilan solishtiriladi; ballar hali ham taqvimdan foydalanadi. |
| `g.ndvi_short` | Satellite NDVI ({nv}/{nt} observations pass quality checks, {rng}) is shown and compared with the crop calendar; the scores still use the calendar. It covers only {yrs:.1f} years, so the seasonal curve is a rough picture, not a climatology. | Sun'iy yo'ldosh NDVI ({nv}/{nt} kuzatuv sifat tekshiruvidan o'tdi, {rng}) ko'rsatiladi va ekin taqvimi bilan solishtiriladi; ballar hali ham taqvimdan foydalanadi. U atigi {yrs:.1f} yilni qamrab oladi, shuning uchun mavsumiy egri chiziq taxminiy ko'rinish, ko'p yillik me'yor emas. |
| `g.ndvi_na` | Vegetation (MODIS NDVI) not loaded: bare periods come from crop calendars, not satellite. ({detail}) | O'simlik qoplami (MODIS NDVI) yuklanmagan: yalang davrlar sun'iy yo'ldoshdan emas, ekin taqvimidan olinadi. ({detail}) |
| `g.smap_info` | SMAP soil moisture ({rng}) is shown for information; the scores do not use it. | SMAP tuproq namligi ({rng}) ma'lumot uchun ko'rsatiladi; ballar undan foydalanmaydi. |
| `g.smap_short` | SMAP soil moisture loaded ({rng}) but it covers only {yrs:.1f} years: a wetter/drier-than-normal anomaly needs at least {minyrs} years, so none is shown; NASA POWER root-zone wetness (GWETROOT, model-based, ~50 km) is shown instead. | SMAP tuproq namligi yuklandi ({rng}), lekin u atigi {yrs:.1f} yilni qamrab oladi: me'yordan nam/quruq og'ishni hisoblash uchun kamida {minyrs} yil kerak, shuning uchun ko'rsatilmaydi; o'rniga NASA POWER ildiz qatlami namligi (GWETROOT, model asosida, ~50 km) ko'rsatiladi. |
| `g.smap_na` | SMAP soil moisture is not usable for this field ({detail}); NASA POWER root-zone wetness (GWETROOT, a model estimate on a ~50 km grid, not a satellite measurement) is shown instead. | Bu dala uchun SMAP tuproq namligidan foydalanib bo'lmaydi ({detail}); o'rniga NASA POWER ildiz qatlami namligi (GWETROOT, ~50 km katakdagi model bahosi, sun'iy yo'ldosh o'lchovi emas) ko'rsatiladi. |
| `g.srtm` | Slope/erosion terrain (SRTM) not loaded: erosion score uses crop cover only. | Nishablik/eroziya relyefi (SRTM) yuklanmagan: eroziya bali faqat ekin qoplamiga asoslanadi. |
| `g.irr_salt` | Irrigation water availability and soil salinity are unknown for this field. | Bu dala uchun sug'orish suvi mavjudligi va tuproq sho'rligi noma'lum. |
| `g.et0` | ET0 is computed from NASA POWER (MERRA-2) variables; it can differ from station-based ET0. | ET0 NASA POWER (MERRA-2) ko'rsatkichlaridan hisoblanadi; meteostansiya asosidagi ET0 dan farq qilishi mumkin. |
| `g.classes` | Dry/normal/wet classes use irrigation demand (crop water need minus effective rain); actual water supply (rivers, snowmelt, canals) is not observed - use the irrigation-supply slider. | Qurg'oqchil/me'yoriy/seryog'in yil sinflari sug'orish talabiga (ekinning suv ehtiyoji minus samarali yog'in) asoslanadi; haqiqiy suv ta'minoti (daryolar, qor erishi, kanallar) hisobga olinmaydi - sug'orish suvi ta'minoti slayderidan foydalaning. |
| `g.temps` | Temperatures come from ~50 km reanalysis (MERRA-2) that runs hot over irrigated land, so hot-day counts and ET0 are likely overstated. | Harorat ~50 km li qayta tahlildan (MERRA-2) olinadi; u sug'oriladigan yerlarda issiqroq chiqadi, shuning uchun issiq kunlar soni va ET0 oshirib ko'rsatilgan bo'lishi mumkin. |
| `g.params` | Crop parameters are approximate regional values, not field trials. | Ekin ko'rsatkichlari mintaqaviy taxminiy qiymatlar, dala tajribalari natijasi emas. |
| `g.power_gaps` | POWER has gaps in: {cols}. | POWER ma'lumotlarida quyidagilar bo'yicha bo'shliqlar bor: {cols}. |
| `g.nosat` | no satellite NDVI/SMAP point has been requested for this preset field | bu tayyor dala uchun sun'iy yo'ldosh NDVI/SMAP nuqtasi so'ralmagan |
| `g.nopoint` | no point within {d} deg of ({lat}, {lon}); nearest is {near} deg away | ({lat}, {lon}) nuqtadan {d} daraja ichida nuqta yo'q; eng yaqini {near} daraja uzoqda |
| `g.approx` | Crop values marked approximate for: {list}. | Quyidagilar bo'yicha ekin qiymatlari taxminiy deb belgilangan: {list}. |
| `d.adds` | adds {crop} | {crop} qo'shiladi |
| `d.adds_bare` | adds {crop} in a bare window | {crop} yalang davrga qo'shiladi |
| `d.adds_break` | adds {crop} to break the cycle | {crop} tsiklni buzish uchun qo'shiladi |
| `d.repl_income` | replaces {old} with the higher-value {new} | {old} o'rniga daromadliroq {new} ekiladi |
| `d.repl_drought` | replaces {old} with the more drought-tolerant {new} | {old} o'rniga qurg'oqchilikka chidamliroq {new} ekiladi |
| `d.pinned` | pinned: {crops} | tanlangan: {crops} |
| `f.early` | {crop} sown (day {day}) before typical last frost (day {frost:.0f}) | {crop} odatdagi oxirgi sovuqdan oldin ekilgan (kun {day}; oxirgi sovuq kuni {frost:.0f}) |
| `f.late` | {crop} matures after typical first autumn frost | {crop} odatdagi birinchi kuzgi sovuqdan keyin pishadi |
| `f.gdd` | {crop}: only {gdd:.0f} GDD available vs ~{req} needed | {crop}: faqat {gdd:.0f} GDD mavjud, ~{req} kerak |
| `x.title_cur` |   (your current rotation) |   (hozirgi almashlab ekishingiz) |
| `x.why_current` | This is what you grow now. It is the baseline every other option is compared against. | Hozir siz shuni ekasiz. Boshqa barcha variantlar shu bilan solishtiriladi. |
| `x.why_legume` | {detail}: a nitrogen-fixing legume (about {n} kg N/ha credit for the next crop, approximate) that also breaks the pest and disease cycle. | {detail}: azot to'playdigan dukkakli ekin (keyingi ekin uchun taxminan {n} kg N/ga hissa, taxminiy), u zararkunanda va kasallik tsiklini ham uzadi. |
| `x.why_cover` | {detail}. Your current rotation leaves the field bare about {now:.0f} days a year; this brings it to about {new:.0f}. | {detail}. Hozirgi almashlab ekishda dala yiliga taxminan {now:.0f} kun yalang qoladi; bu variantda taxminan {new:.0f} kun. |
| `x.why_drought` | {detail}, aimed at water scarcity. {eff} | {detail}, suv tanqisligiga qaratilgan. {eff} |
| `x.eff_down` | Estimated irrigation need falls by {d:.0f} mm/year. | Taxminiy sug'orish ehtiyoji yiliga {d:.0f} mm ga kamayadi. |
| `x.eff_up` | Note: estimated irrigation need is NOT lower here ({d:+.0f} mm/year vs today), because the cycle fits more crop-days per year; the benefit is a more drought-tolerant crop. | Eslatma: bu yerda taxminiy sug'orish ehtiyoji kam EMAS (hozirgidan {d:+.0f} mm/yil), chunki tsiklga yiliga ko'proq ekin kunlari sig'adi; foydasi - qurg'oqchilikka chidamliroq ekin. |
| `x.why_perennial` | {detail}: a deep-rooted perennial legume that builds organic matter, fixes nitrogen and covers the soil. | {detail}: chuqur ildizli ko'p yillik dukkakli ekin; organik modda to'playdi, azot to'playdi va tuproqni qoplaydi. |
| `x.why_winter` | {detail}: a winter crop that uses the cool, wetter months and changes the crop family sequence. | {detail}: salqin va namroq oylardan foydalanadigan kuzgi ekin; ekin oilalari ketma-ketligini o'zgartiradi. |
| `x.ev_cal` | Calendar: field is bare about {new:.0f} days/year in this rotation (current: {now:.0f}); cycle length {years} year(s). | Taqvim: bu almashlab ekishda dala yiliga taxminan {new:.0f} kun yalang (hozirgi: {now:.0f}); tsikl uzunligi {years} yil. |
| `x.ev_sat` | Satellite check (MODIS NDVI below 0.2, counting only days with a clear observation): about {obs:.0f} bare days/year, against {now:.0f} from the crop calendar; about {unobs:.0f} days/year have no clear observation. | Sun'iy yo'ldosh tekshiruvi (MODIS NDVI 0,2 dan past, faqat aniq kuzatuv bo'lgan kunlar hisobga olinadi): yiliga taxminan {obs:.0f} yalang kun, ekin taqvimida esa {now:.0f}; yiliga taxminan {unobs:.0f} kunda aniq kuzatuv yo'q. |
| `x.ev_clim` | Climate at the field ({y0}–{y1}, NASA POWER): median {frost:.0f} frost days/year (last spring frost ~day {last:.0f}, first autumn frost ~day {first:.0f}), {heat:.0f} days/year with Tmax ≥ 35 °C, rainfall {rain:.0f} mm vs reference ET0 {et0:.0f} mm. | Dalaning iqlimi ({y0}–{y1}, NASA POWER): yiliga o'rtacha {frost:.0f} sovuq kun (oxirgi bahorgi sovuq ~{last:.0f}-kun, birinchi kuzgi sovuq ~{first:.0f}-kun), yiliga {heat:.0f} kun Tmax ≥ 35 °C, yog'in {rain:.0f} mm, taqqoslash uchun ET0 {et0:.0f} mm. |
| `x.ev_fit` | {label}: {med:.0f} (typical range {p10:.0f}–{p90:.0f}); dry years {dry:.0f}, normal {normal:.0f}, wet {wet:.0f}. Current rotation: {cur:.0f}. This is a relative score among the options shown, not an absolute grade. | {label}: {med:.0f} (odatiy oraliq {p10:.0f}–{p90:.0f}); qurg'oqchil yillarda {dry:.0f}, me'yoriy yillarda {normal:.0f}, seryog'in yillarda {wet:.0f}. Hozirgi almashlab ekish: {cur:.0f}. Bu ko'rsatilgan variantlar orasidagi nisbiy ball, mutlaq baho emas. |
| `x.ev_irr` | Estimated irrigation need: {irr:.0f} mm/year{cmp}; dry years {dry:.0f}, wet years {wet:.0f}. | Taxminiy sug'orish ehtiyoji: yiliga {irr:.0f} mm{cmp}; qurg'oqchil yillarda {dry:.0f}, seryog'in yillarda {wet:.0f}. |
| `x.ev_irr_cmp` |  ({pct:+.0f}% vs current {cur:.0f} mm) |  (hozirgisiga nisbatan {pct:+.0f}%, hozirgi {cur:.0f} mm) |
| `x.ev_n` | Nitrogen credit from legumes: about {n:.0f} kg N/ha per year (approximate). | Dukkakli ekinlardan azot hissasi: yiliga taxminan {n:.0f} kg N/ga (taxminiy). |
| `x.ev_yield` | Yield at risk from water shortage (FAO yield-response): {med:.0f}% typical, {p90:.0f}% in the worst 1 year in 10 (irrigation supply set to the slider value). | Suv yetishmasligidan hosil xavfi (FAO hosil-javob usuli): odatda {med:.0f}%, 10 yilning eng yomon 1 yilida {p90:.0f}% (sug'orish ta'minoti slayderdagi qiymatga teng). |
| `x.ev_heat` | Heat exposure, {crop}: {n:.0f} days above {thr:.0f} °C in season (worst 1 in 10: {p90:.0f}); not converted to yield loss. | Issiqqa duchor bo'lish, {crop}: mavsumda {thr:.0f} °C dan yuqori {n:.0f} kun (10 yilning eng yomonida: {p90:.0f}); hosil yo'qotilishiga aylantirilmagan. |
| `x.ev_suit` | Climate fit {suit:.0f}/100; pest-cycle break {pest:.0f}/100. | Iqlimga moslik {suit:.0f}/100; zararkunanda tsiklini uzish {pest:.0f}/100. |
| `x.ev_ties` | No real difference between these options for: {list} (treated as a tie). | Bu variantlar orasida quyidagilar bo'yicha haqiqiy farq yo'q: {list} (teng deb olingan). |
| `x.b_better` | {label}: better than your current rotation (relative score {new:.0f} vs {old:.0f}). | {label}: hozirgi almashlab ekishingizdan yaxshiroq (nisbiy ball {new:.0f}, hozirgisi {old:.0f}). |
| `x.t_worse` | {label}: worse than your current rotation (relative score {new:.0f} vs {old:.0f}). | {label}: hozirgi almashlab ekishingizdan yomonroq (nisbiy ball {new:.0f}, hozirgisi {old:.0f}). |
| `x.b_bare` | Bare soil reduced from ~{now:.0f} to ~{new:.0f} days/year. | Yalang tuproq yiliga ~{now:.0f} kundan ~{new:.0f} kungacha kamayadi. |
| `x.b_none` | No priority improves by 5+ points over the current rotation with your weights. | Siz tanlagan vaznlarda hech bir ustuvorlik hozirgi almashlab ekishdan 5+ ballga yaxshilanmaydi. |
| `x.b_known` | Known to you; no new equipment, seed or market arrangements needed. | Sizga tanish; yangi texnika, urug' yoki bozor kelishuvlari kerak emas. |
| `x.t_lowest` | Lowest among the options on: {list}. | Variantlar orasida eng past: {list}. |
| `x.r_salt` | {crop} is salt-sensitive; check soil/irrigation-water salinity locally. | {crop} tuzga sezgir; tuproq va sug'orish suvi sho'rligini joyida tekshiring. |
| `x.r_new` | New crop {crop}: confirm seed availability, machinery, and local agronomy advice. | Yangi ekin {crop}: urug' mavjudligi, texnika va mahalliy agronom maslahatini aniqlang. |
| `x.r_market` | Market ({crop}): {note} | Bozor ({crop}): {note} |
| `x.r_irr` | Irrigation water supply and timing were not modelled; confirm with your water-user association. | Sug'orish suvi ta'minoti va muddatlari modellashtirilmagan; suv iste'molchilari uyushmasi bilan aniqlang. |
| `mk.cotton` | Often sold via contracts/clusters; check current procurement terms and prices. | Ko'pincha shartnoma/klaster orqali sotiladi; joriy xarid shartlari va narxlarni tekshiring. |
| `mk.winter_wheat` | Food-security crop; procurement/quota rules may apply locally. | Oziq-ovqat xavfsizligi ekini; joyida xarid/kvota qoidalari amal qilishi mumkin. |
| `mk.barley` | Feed/malting market; lower price than wheat in most regions. | Em-xashak/solod bozori; ko'p hududlarda bug'doydan arzon. |
| `mk.maize` | Strong feed demand; drying/storage costs matter. | Em-xashak uchun talab kuchli; quritish va saqlash xarajatlari muhim. |
| `mk.sorghum` | Thin local market in some regions; feed use; check buyers. | Ba'zi hududlarda mahalliy bozor kichik; em-xashak sifatida ishlatiladi; xaridorlarni tekshiring. |
| `mk.millet` | Small niche market; mostly feed/food local use. | Kichik maxsus bozor; asosan mahalliy em-xashak/oziq-ovqat uchun. |
| `mk.alfalfa` | Local hay/feed demand; livestock needed or hay sold; seed cost. | Pichan/em-xashakka mahalliy talab; chorva kerak yoki pichan sotiladi; urug' narxi. |
| `mk.mung_bean` | Often grown as post-wheat short-season crop; check buyers/export prices. | Ko'pincha bug'doydan keyin qisqa mavsumli ekin sifatida ekiladi; xaridorlar/eksport narxlarini tekshiring. |
| `mk.chickpea` | Good export demand historically; price volatile. | Tarixan eksport talabi yaxshi; narx o'zgaruvchan. |
| `mk.lentil` | Export/food market; check local buyers. | Eksport/oziq-ovqat bozori; mahalliy xaridorlarni tekshiring. |
| `mk.soybean` | Large commodity market in the US; limited processing in Central Asia. | AQShda katta tovar bozori; Markaziy Osiyoda qayta ishlash cheklangan. |
| `mk.sunflower` | Oil crush demand; check local processors. | Moy ishlab chiqarish uchun talab; mahalliy qayta ishlovchilarni tekshiring. |
| `mk.safflower` | Niche oil/dye market; few buyers in many regions. | Moy/bo'yoq uchun maxsus bozor; ko'p hududlarda xaridor kam. |
| `mk.rapeseed` | Oil crush demand; needs a nearby processor; winter-kill risk. | Moy uchun talab; yaqin atrofda qayta ishlovchi kerak; qishda nobud bo'lish xavfi. |
| `mk.rye_cover` | No direct sale; ~USD 60-100/ha seed+termination (rough); may be grazed. | To'g'ridan-to'g'ri sotilmaydi; urug' va yo'q qilish ~60-100 AQSh dollari/ga (taxminiy); yaylov sifatida ishlatilishi mumkin. |
| `mk.hairy_vetch` | No direct sale; seed costly/hard to find (~USD 100/ha incl. termination, rough); N credit for next crop. | To'g'ridan-to'g'ri sotilmaydi; urug'i qimmat/topish qiyin (yo'q qilish bilan ~100 AQSh dollari/ga, taxminiy); keyingi ekin uchun azot hissasi. |
| `mk.clover` | Forage value (hay/grazing); seed availability varies. | Em-xashak qiymati (pichan/yaylov); urug' mavjudligi turlicha. |
| `mk.potato` | High value but high cost, storage and price risk. | Qiymati yuqori, lekin xarajat, saqlash va narx xavfi ham yuqori. |
| `mk.melon` | High value local/regional demand; labour intensive; perishable. | Mahalliy/mintaqaviy talab yuqori; ko'p mehnat talab qiladi; tez buziladi. |
| `mk.sugar_beet` | Needs a sugar factory within reach; contract-based. | Yaqin atrofda shakar zavodi kerak; shartnoma asosida. |
| `ui.nasa` | Built on NASA Earth observation data | NASA Yer kuzatuvi ma'lumotlari asosida |
| `ui.lang` | Language / Til | Language / Til |
| `ui.field_label` | Field | Dala |
| `ui.field_help` | Type to search the demo and regional fields, or choose “My own location” and enter coordinates. | Tayyor va mintaqaviy dalalarni qidirish uchun yozing yoki “O'z joylashuvim”ni tanlab koordinatalarni kiriting. |
| `ui.selected` | Selected field | Tanlangan dala |
| `ui.grows` | Grows now | Hozir ekiladi |
| `ui.cta` | Compare rotation options | Almashlab ekish variantlarini solishtirish |
| `ui.hero` | See how a different crop rotation could change water use, soil and income on this field, using NASA climate and satellite data. | NASA iqlim va sun'iy yo'ldosh ma'lumotlari yordamida boshqa almashlab ekish shu dalada suv sarfi, tuproq va daromadni qanday o'zgartirishi mumkinligini ko'ring. |
| `ui.chip_power` | NASA POWER climate {rng} | NASA POWER iqlimi {rng} |
| `ui.chip_ndvi_on` | MODIS NDVI loaded | MODIS NDVI yuklangan |
| `ui.chip_ndvi_off` | MODIS NDVI not loaded | MODIS NDVI yuklanmagan |
| `ui.chip_smap_on` | SMAP soil moisture loaded | SMAP tuproq namligi yuklangan |
| `ui.chip_smap_off` | SMAP not usable here | SMAP bu yerda yaroqsiz |
| `ui.chip_soil_on` | SoilGrids soil data | SoilGrids tuproq ma'lumotlari |
| `ui.chip_soil_off` | Soil data unavailable | Tuproq ma'lumotlari mavjud emas |
| `ui.sidebar_rot` | Your rotation | Sizning almashlab ekishingiz |
| `ui.sidebar_prio` | Your priorities | Sizning ustuvorliklaringiz |
| `ui.sec_overview` | Climate at this field | Dalaning iqlimi |
| `ui.sec_overview_sub` | Typical year, from the daily NASA POWER record. Ranges show the 10th–90th percentile across years. | Odatdagi yil, NASA POWER kunlik yozuvidan. Oraliqlar yillar bo'yicha 10–90-protsentilni ko'rsatadi. |
| `ui.sec_history` | Climate history | Iqlim tarixi |
| `ui.sec_season` | Your current rotation through the year | Hozirgi almashlab ekishingiz yil davomida |
| `ui.sec_soil` | Soil and soil moisture | Tuproq va tuproq namligi |
| `ui.sec_compare` | Rotation options at a glance | Almashlab ekish variantlari bir qarashda |
| `ui.sec_cards` | Each option in detail | Har bir variant batafsil |
| `ui.kpi_rain` | Rainfall | Yog'in |
| `ui.kpi_rain_d` | Total precipitation in a typical year. | Odatdagi yildagi umumiy yog'in miqdori. |
| `ui.kpi_range` | Range {lo:.0f}–{hi:.0f} {unit} | Oraliq {lo:.0f}–{hi:.0f} {unit} |
| `ui.kpi_et0_d` | Water a well-watered reference crop loses to the air in a year (FAO-56). | Yaxshi sug'orilgan standart ekin yil davomida havoga yo'qotadigan suv (FAO-56). |
| `ui.kpi_et0_gap` | Exceeds rainfall by {gap:.0f} mm; rain covers {pct:.0f}% of it | Yog'indan {gap:.0f} mm ko'p; yog'in uning {pct:.0f}% ini qoplaydi |
| `ui.kpi_et0_ok` | Rainfall exceeds ET0 by {gap:.0f} mm | Yog'in ET0 dan {gap:.0f} mm ko'p |
| `ui.kpi_last` | Last spring frost | Oxirgi bahorgi qirov |
| `ui.kpi_last_d` | Typical last day with a minimum at or below 0 °C. | Eng past harorat 0 °C va undan past bo'lgan odatdagi oxirgi kun. |
| `ui.kpi_first` | First autumn frost | Birinchi kuzgi qirov |
| `ui.kpi_first_d` | Typical first day with a minimum at or below 0 °C. | Eng past harorat 0 °C va undan past bo'lgan odatdagi birinchi kun. |
| `ui.kpi_dates` | Usually between {a} and {b} | Odatda {a} va {b} oralig'ida |
| `ui.kpi_frost` | Frost days | Qirovli kunlar |
| `ui.kpi_frost_d` | Days per year with a minimum at or below 0 °C. | Yilda eng past harorat 0 °C va undan past bo'lgan kunlar. |
| `ui.kpi_hot` | Very hot days | Juda issiq kunlar |
| `ui.kpi_hot_d` | Days per year with a maximum of 35 °C or more. | Yilda eng yuqori harorat 35 °C va undan yuqori bo'lgan kunlar. |
| `ui.kpi_hot_ctx` | Range {lo:.0f}–{hi:.0f}; likely overstated (reanalysis runs hot) | Oraliq {lo:.0f}–{hi:.0f}; ehtimol oshirilgan (qayta tahlil issiqroq chiqaradi) |
| `ui.kpi_temp` | Mean temperature | O'rtacha harorat |
| `ui.kpi_temp_d` | Average daily air temperature over the year. | Yil davomidagi o'rtacha kunlik havo harorati. |
| `ui.kpi_temp_ctx` | {dt:+.2f} °C per decade ({clear} trend) | O'n yilda {dt:+.2f} °C ({clear}) |
| `ui.unit_days` | days/yr | kun/yil |
| `ui.unit_mm` | mm/yr | mm/yil |
| `ui.unit_c` | °C | °C |
| `ui.tbl_metric` | Measure | Ko'rsatkich |
| `ui.tbl_fit` | Fit to your priorities (0–100) | Ustuvorliklarga moslik (0–100) |
| `ui.tbl_irr` | Irrigation need (mm/yr) | Sug'orish ehtiyoji (mm/yil) |
| `ui.tbl_bare` | Bare soil (days/yr) | Ochiq tuproq (kun/yil) |
| `ui.tbl_n` | Nitrogen from legumes (kg N/ha/yr) | Dukkakli ekinlardan azot (kg N/ga/yil) |
| `ui.tbl_yield` | Yield at risk from water shortage, typical / bad year | Suv yetishmasligidan hosil xavfi, odatda / yomon yil |
| `ui.tbl_dry` | Fit in dry / normal / wet years | Qurg'oqchil / me'yoriy / seryog'in yillarda moslik |
| `ui.tbl_best` | Best of the options shown on this measure | Ko'rsatilgan variantlar orasida shu ko'rsatkich bo'yicha eng yaxshisi |
| `ui.notice` | Decision support: it supports, and does not replace, your judgment and that of a local agronomist. | Qarorlarni qo'llab-quvvatlash: u sizning va mahalliy agronomning fikrini qo'llab-quvvatlaydi, o'rnini bosmaydi. |
| `ui.chart_temp` | Temperature through the year | Yil davomida harorat |
| `ui.t_max` | Daily maximum | Kunlik maksimum |
| `ui.t_mean` | Daily mean | Kunlik o'rtacha |
| `ui.t_min` | Daily minimum | Kunlik minimum |
| `ui.t_y` | Temperature (°C) | Harorat (°C) |
| `ui.chart_frost` | Frost risk by week | Haftalar bo'yicha qirov xavfi |
| `ui.chart_heat` | Very hot days by month | Oylar bo'yicha juda issiq kunlar |
| `ui.kpi_free` | Frost-free period | Qirovsiz davr |
| `ui.kpi_free_d` | Days between the last spring and the first autumn frost in a typical year. | Odatdagi yilda oxirgi bahorgi va birinchi kuzgi qirov orasidagi kunlar. |
| `ui.kpi_free_ctx` | Range {lo:.0f}–{hi:.0f} days | Oraliq {lo:.0f}–{hi:.0f} kun |
| `ui.opt_n` | Option {n} | {n}-variant |
| `ui.heat_h` | Heat exposure | Issiqqa duchor bo'lish |
| `ui.best_note` | Shaded cells mark the best value among the options shown for that measure; unshaded rows are tied. | Rangli kataklar ko'rsatilgan variantlar orasida shu ko'rsatkich bo'yicha eng yaxshi qiymatni bildiradi; rangsiz qatorlarda farq yo'q. |
| `ui.back` | Back to your field | Dalaga qaytish |
| `col.hot2` | Hot days in season (above the crop's heat threshold) | Mavsumdagi issiq kunlar (ekinning issiqlik chegarasidan yuqori) |
| `ui.data_h` | Data sources | Ma'lumot manbalari |
| `ui.st_ok` | Loaded | Yuklangan |
| `ui.st_miss` | Unavailable | Mavjud emas |
| `ui.st_na` | Not applicable | Qo'llanilmaydi |
| `ui.ds_power` | NASA POWER climate | NASA POWER iqlimi |
| `ui.ds_ndvi` | MODIS vegetation (NDVI) | MODIS o'simlik qoplami (NDVI) |
| `ui.ds_smap` | SMAP soil moisture | SMAP tuproq namligi |
| `ui.ds_soil` | SoilGrids soil | SoilGrids tuprog'i |
| `ui.tip_power` | Daily climate record {rng}. | Kunlik iqlim yozuvi {rng}. |
| `ui.tip_na` | No satellite point was requested for this field, so this layer does not apply here. | Bu dala uchun sun'iy yo'ldosh nuqtasi so'ralmagan, shuning uchun bu qatlam bu yerda qo'llanilmaydi. |
| `ui.tip_ndvi_ok` | Satellite greenness is shown next to the crop calendar. | Sun'iy yo'ldosh yashilligi ekin taqvimi yonida ko'rsatiladi. |
| `ui.tip_ndvi_miss` | No usable satellite file for this place; bare periods come from the crop calendar. | Bu joy uchun yaroqli sun'iy yo'ldosh fayli yo'q; ochiq davrlar ekin taqvimidan olinadi. |
| `ui.tip_smap_ok` | Soil-moisture anomaly from satellite retrievals. | Sun'iy yo'ldosh o'lchovlaridan tuproq namligi og'ishi. |
| `ui.tip_smap_miss` | No usable satellite retrievals here; NASA POWER root-zone wetness is shown instead. | Bu yerda yaroqli sun'iy yo'ldosh o'lchovlari yo'q; o'rniga NASA POWER ildiz qatlami namligi ko'rsatiladi. |
| `ui.tip_soil_ok` | Texture, organic carbon and pH are shown for information. | Tuproq tarkibi, organik uglerod va pH ma'lumot uchun ko'rsatiladi. |
| `ui.tip_soil_miss` | SoilGrids could not be reached and no manual reading was found. | SoilGrids'ga ulanib bo'lmadi va qo'lda kiritilgan qiymat topilmadi. |
| `ui.data_note` | Layers marked unavailable or not applicable do not change the scores; they are shown for information. See the full list under “What data is missing”. | Mavjud emas yoki qo'llanilmaydi deb belgilangan qatlamlar ballarga ta'sir qilmaydi; ular ma'lumot uchun ko'rsatiladi. To'liq ro'yxat “Qanday ma'lumotlar yetishmayapti” bo'limida. |
| `ui.hemi_n` | N | Sh |
| `ui.hemi_s` | S | J |
| `ui.hemi_w` | W | G' |
| `ui.kpi_rtrend` | Rainfall trend | Yog'in tendensiyasi |
| `ui.kpi_rtrend_d` | Change in yearly rainfall per decade over the record ({y0}–{y1}). | Yillik yog'inning yozuv davridagi ({y0}–{y1}) o'n yillikdagi o'zgarishi. |
| `ui.unit_mm_dec` | mm/decade | mm/o'n yil |
| `ui.kpi_extremes` | Frost and heat | Qirov va issiqlik |
| `ui.grp_econ` | Income and feed | Daromad va em-xashak |
| `ui.prio_hint` | Move a slider up for what matters more to you. | Siz uchun muhimroq narsani slayderni yuqoriga surib belgilang. |
| `ui.step_rot` | Choose the crops you grow, in order. | Ekadigan ekinlaringizni tartib bilan tanlang. |
| `ui.next_h` | Next: compare rotation options | Keyingi qadam: almashlab ekish variantlarini solishtiring |
| `ui.next_t` | See how other rotations compare with yours on water, soil and income. | Boshqa almashlab ekishlar sizniki bilan suv, tuproq va daromad bo'yicha qanday solishtirilishini ko'ring. |
| `ui.best_fit` | Best fit | Eng mos |
| `ui.g_main` | Overall | Umumiy |
| `ui.g_water` | Water and climate | Suv va iqlim |
| `ui.g_soil` | Soil and cover | Tuproq va qoplama |
| `ui.g_prio` | Relative score by priority (0–100) | Ustuvorlik bo'yicha nisbiy ball (0–100) |
| `ui.back_field` | Back to your field | Dalaga qaytish |
| `ui.step_trail` | 1 Field  ›  2 Climate  ›  3 Compare options  ›  4 Trade-offs | 1 Dala  ›  2 Iqlim  ›  3 Variantlarni solishtirish  ›  4 Foyda va kamchiliklar |
| `map.base_sat` | Satellite | Sun'iy yo'ldosh |
| `map.base_street` | Street map | Ko'cha xaritasi |
| `map.base_terrain` | Terrain | Relyef |
| `map.layer_ndvi` | Vegetation (NDVI) | O'simlik qoplami (NDVI) |
| `map.layer_precip` | Rainfall rate | Yog'in jadalligi |
| `map.layer_temp` | Land surface temperature | Yer yuzasi harorati |
| `map.layer_soil` | Surface soil moisture | Yuza tuproq namligi |
| `map.title_ndvi` | Vegetation greenness (NDVI) | O'simlik yashilligi (NDVI) |
| `map.title_precip` | Precipitation rate (IMERG) | Yog'in jadalligi (IMERG) |
| `map.title_temp` | Land surface temperature, daytime | Yer yuzasi harorati, kunduzi |
| `map.title_soil` | Surface soil moisture (SMAP L4) | Yuza tuproq namligi (SMAP L4) |
| `map.src_ndvi` | NASA GIBS · MODIS Terra, rolling 8-day, 250 m | NASA GIBS · MODIS Terra, 8 kunlik, 250 m |
| `map.src_precip` | NASA GIBS · GPM IMERG, ~10 km | NASA GIBS · GPM IMERG, ~10 km |
| `map.src_temp` | NASA GIBS · MODIS Terra, 8-day composite, 1 km | NASA GIBS · MODIS Terra, 8 kunlik kompozit, 1 km |
| `map.src_soil` | NASA GIBS · SMAP Level 4, ~9 km | NASA GIBS · SMAP 4-daraja, ~9 km |
| `map.note_ndvi` | Higher is greener. Clouds can leave gaps in a composite. | Qiymat qancha yuqori bo'lsa, shuncha yashil. Bulutlar kompozitda bo'shliqlar qoldirishi mumkin. |
| `map.note_precip` | Rate in mm per hour for the observation day, not a seasonal total. | Kuzatuv kuni uchun soatiga mm dagi jadallik, mavsumiy jami emas. |
| `map.note_temp` | Temperature of the ground surface, not of the air. | Yer yuzasining harorati, havo harorati emas. |
| `map.note_soil` | Model analysis that assimilates SMAP data (top ~5 cm), not a direct measurement. | SMAP ma'lumotlarini o'zlashtiruvchi model tahlili (yuqori ~5 sm), to'g'ridan-to'g'ri o'lchov emas. |
| `map.short_ndvi` | NDVI | NDVI |
| `map.short_precip` | Rain | Yog'in |
| `map.short_temp` | Surface temp. | Yuza harorati |
| `map.short_soil` | Soil moisture | Tuproq namligi |
| `map.loading` | Loading tiles… | Plitkalar yuklanmoqda… |
| `map.loaded` | Loaded | Yuklandi |
| `map.tile_error` | Some tiles could not be loaded (network, or no data here). | Ba'zi plitkalar yuklanmadi (tarmoq yoki bu yerda ma'lumot yo'q). |
| `map.source` | Source | Manba |
| `map.date` | Observation date | Kuzatuv sanasi |
| `map.stale` | from a saved copy | saqlangan nusxadan |
| `map.unavailable` | unavailable | mavjud emas |
| `map.help` | Click the map to move the field. The layers button (top right) switches the basemap or shows a NASA data layer. | Dalani ko'chirish uchun xaritani bosing. Qatlamlar tugmasi (yuqori o'ng) xarita asosini almashtiradi yoki NASA ma'lumot qatlamini ko'rsatadi. |
| `map.layers_h` | NASA layers (latest observation) | NASA qatlamlari (oxirgi kuzatuv) |
| `map.stale_note` | * Latest observation known on {d} (saved copy). It refreshes from NASA GIBS in the background when reachable. | * {d} sanasida ma'lum bo'lgan oxirgi kuzatuv (saqlangan nusxa). NASA GIBS'ga ulanish mumkin bo'lganda fonda yangilanadi. |
| `map.asof` | * Latest observation known on {d}; may be newer on NASA GIBS. | * {d} sanasida ma'lum bo'lgan oxirgi kuzatuv; NASA GIBS'da yangiroq bo'lishi mumkin. |
| `map.scope` | Layers are global satellite or model images shown at their own resolution. The climate figures on this page come from NASA POWER (~50 km) and do not change with the layer. | Qatlamlar o'z aniqligida ko'rsatiladigan global sun'iy yo'ldosh yoki model tasvirlari. Sahifadagi iqlim ko'rsatkichlari NASA POWER'dan (~50 km) olinadi va qatlamga bog'liq emas. |
| `map.marker` | Selected field | Tanlangan dala |
| `g.ndvi_notcrop` | the NDVI at this point peaks at only {peak:.2f} in a typical year (below {thr:.1f}), so the pixel is not clearly cropland (bare ground, town edge or water) and is not used | bu nuqtadagi NDVI odatdagi yilda atigi {peak:.2f} gacha ko'tariladi ({thr:.1f} dan past), shuning uchun piksel aniq ekin maydoni emas (yalang yer, shahar chekkasi yoki suv) va ishlatilmaydi |
| `g.joined` | {items} | {items} |
| `f.ndvi_anytime` | scattered through the year | yil davomida tarqoq |
| `g.r_rejected` | all observations rejected by QA | barcha kuzatuvlar sifat tekshiruvidan o'tmadi |
| `g.r_nofile` | no satellite file found (download it from AppEEARS) | sun'iy yo'ldosh fayli topilmadi (AppEEARS'dan yuklab oling) |
| `g.r_unreadable` | the satellite file could not be read | sun'iy yo'ldosh faylini o'qib bo'lmadi |
| `soil.src_rest` | SoilGrids (REST service) | SoilGrids (REST xizmati) |
| `soil.src_manual` | SoilGrids web map, read manually | SoilGrids veb-xaritasi, qo'lda o'qilgan |
| `ui.view_label` | View | Ko'rinish |
| `map.zoom_in` | Zoom in | Yaqinlashtirish |
| `map.zoom_out` | Zoom out | Uzoqlashtirish |
| `ui.elev_tip` | Average elevation of the ~50 km NASA POWER climate cell around the point, not the elevation of this field. | Nuqta atrofidagi ~50 km li NASA POWER iqlim katagining o'rtacha balandligi, bu dalaning balandligi emas. |

## 4. What is NOT translated (stays English in Uzbek mode)

- Technical detail inside a data-loading message that is not one of the known patterns (e.g. a file-format error from a satellite CSV) stays as the original English text; the known "no point within ... deg" message is translated.
- Texts inside the downloaded documents (`README.md`, `docs/`).
- Soil texture class names (`clay loam`, `loam`, ...) and the data-source names.
