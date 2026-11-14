# Uzbek text for native-speaker review

All Uzbek text (Latin script) was written by the AI assistant and has **not** been checked by a native speaker. Please correct anything that is wrong, unnatural, or not the term farmers actually use. Placeholders in `{braces}` (numbers, crop names) must stay exactly as they are. Dataset and product names (NASA POWER, MODIS, SMAP, SoilGrids, FAO) are intentionally not translated.

To change a string, edit `src/fieldshift/i18n.py` (key shown below); `scripts/uzbek_review.py` regenerates this file.


## 1. Strings I am unsure about (37)

| key | English | Uzbek | why unsure |
|---|---|---|---|
| `ex.gaps` | Information gaps | Ma'lumot bo'shliqlari | 'bo'shliqlar' for information gaps |
| `f.trend` | **Trend {y0}–{y1}:** temperature {dt:+.2f} °C per decade ({tclear} trend); rain {dp:+.0f} mm per decade ({pclear} trend). | **Yo'nalish {y0}–{y1}:** harorat o'n yilda {dt:+.2f} °C ({tclear}); yog'in o'n yilda {dp:+.0f} mm ({pclear}). | 'trend' as 'yo'nalish' |
| `field.kansas` | Central Kansas, USA | Markaziy Kanzas, AQSH | 'Kanzas' spelling; 'AQSH' for USA |
| `g.versus_text` | • Climate values come from a ~50 km model/satellite blend, not from a weather station at your field. Over irrigated land it tends to run hotter and drier than the ground.<br>• Irrigation need and ET0 are computed (FAO-56 Penman–Monteith), not measured.<br>• Crop values (water use, heat limits, nitrogen credit) are regional approximations; check them with local advisers.<br>• Water supply from rivers or canals is not observed; use the irrigation-water slider to test shortages. | • Iqlim qiymatlari dalangizdagi ob-havo stansiyasidan emas, ~50 km li model/sun'iy yo'ldosh aralashmasidan olingan. Sug'oriladigan yerlarda u haqiqatdagidan issiqroq va quruqroq chiqishga moyil.<br>• Sug'orish ehtiyoji va ET0 o'lchanmagan, hisoblangan (FAO-56 Penman–Monteith).<br>• Ekin qiymatlari (suv sarfi, issiqlik chegaralari, azot hisobi) mintaqaviy taxminlar; mahalliy maslahatchilar bilan tekshiring.<br>• Daryo yoki kanallardan suv yetkazib berish kuzatilmaydi; suv yetishmasligini sinash uchun sug'orish suvi slayderidan foydalaning. | technical bullets: check terms |
| `gl.dnw.d` | Years sorted into thirds by how much irrigation water crops needed: dry = highest need. | Yillar ekinlar qancha sug'orish suvi talab qilganiga qarab uchga bo'lingan: quruq = eng ko'p talab. | technical explanation: check wording and terms |
| `gl.dnw.t` | Dry / normal / wet year | Quruq / o'rtacha / nam yil | technical term: check the established Uzbek term |
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
| `note.en_only` |  | Variant kartochkalaridagi batafsil izohlar (dalillar, bo'shliqlar, xavflar) hozircha faqat inglizcha. | wording of 'bo'shliqlar' for information gaps |
| `p.forage` | Forage value | Em-xashak qiymati | 'em-xashak' vs 'ozuqa' for forage |
| `p.nitrogen` | Nitrogen fixing | Azot to'plash | 'azot to'plash' vs 'azot biriktirish' for nitrogen fixing |
| `p.soil_om` | Soil organic matter | Tuproqdagi organik moddalar (chirindi) | 'chirindi' (humus) vs 'organik moddalar' |
| `side.whatif` | What if…? | Agar shunday bo'lsa…? | natural phrasing of 'What if…?' |
| `soil.bdod_kg_dm3` | bulk density kg/dm³ | hajmiy zichlik kg/dm³ | 'hajmiy zichlik' for bulk density |
| `soil.clay_pct` | clay % | gil % | soil texture terms: gil/qum/chang |
| `soil.texture` | texture | tuproq turi | texture class names are not translated |
| `sum.tradeoff` | **Main trade-off:** {tradeoff}. | **Asosiy kamchilik:** {tradeoff}. | 'trade-off' rendered as 'kamchilik' (drawback) |
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

## 3. All other strings (189), please still skim

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
| `view.field` | 📍 Your field | 📍 Sizning dalangiz |
| `view.options` | 🔀 Rotation options | 🔀 Almashlab ekish variantlari |
| `view.glossary` | 📖 Glossary & data | 📖 Lug'at va ma'lumotlar |
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
| `f.ndvi_text` | Satellite view: the field is below the bare-soil greenness level about **{obs:.0f} days a year** (the crop calendar above says {cal:.0f}). Differences usually mean sowing dates, weeds or cloud gaps differ from the typical calendar. | Sun'iy yo'ldosh ma'lumoti: dala yiliga taxminan **{obs:.0f} kun** ochiq tuproq yashillik darajasidan past (yuqoridagi ekin taqvimi bo'yicha {cal:.0f}). Farq odatda ekish sanalari, begona o'tlar yoki bulutli kunlar odatdagi taqvimdan farq qilishini bildiradi. |
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
| `o.fit_cap` | {short} · typical range {lo:.0f}–{hi:.0f} · dry {d:.0f} / normal {n:.0f} / wet {w:.0f} | {short} · odatdagi oraliq {lo:.0f}–{hi:.0f} · quruq {d:.0f} / o'rtacha {n:.0f} / nam {w:.0f} |
| `o.irr` | 💧 Irrigation need: <b>{irr:.0f} mm/yr</b>{pct} | 💧 Sug'orish ehtiyoji: <b>{irr:.0f} mm/yil</b>{pct} |
| `o.vs_now` |  ({pct:+.0f}% vs now) |  (hozirgiga nisbatan {pct:+.0f}%) |
| `o.bare` | 🟤 Bare soil: <b>{d:.0f} days/yr</b> | 🟤 Ochiq tuproq: <b>yiliga {d:.0f} kun</b> |
| `o.nitrogen` | 🌱 Nitrogen from legumes: <b>{n:.0f} kg N/ha/yr</b> | 🌱 Dukkakli ekinlardan azot: <b>yiliga {n:.0f} kg N/ga</b> |
| `o.yield` | ⚠️ Yield at risk from water shortage: <b>{m:.0f}%</b> typical, <b>{p:.0f}%</b> in a bad year (1 in 10) | ⚠️ Suv yetishmasligidan hosil xavfi: odatda <b>{m:.0f}%</b>, yomon yilda (10 yilda 1) <b>{p:.0f}%</b> |
| `o.heat` | 🔥 {crop}: <b>{n:.0f}</b> days above {thr:.0f} °C in season (bad year: {p:.0f}) | 🔥 {crop}: mavsumda {thr:.0f} °C dan yuqori <b>{n:.0f}</b> kun (yomon yilda: {p:.0f}) |
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
| `viz.dry` | Dry years (high water need) | Quruq yillar (suv talabi yuqori) |
| `viz.normal` | Normal years | O'rtacha yillar |
| `viz.wet` | Wet years (low water need) | Nam yillar (suv talabi past) |
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

## 4. What is NOT translated (stays English in Uzbek mode)

- The long bullets inside each option card: *Why this option*, *Evidence (numbers)*, *Benefits*, *Information gaps*, *Risks to check with a local expert*. The section titles are translated; the bullet sentences are templated English built from the numbers. The app shows a note about this in Uzbek mode.
- The *What data is missing for this field?* list on the field view (same reason).
- Texts inside the downloaded documents (`README.md`, `docs/`).
- Soil texture class names (`clay loam`, `loam`, ...) and the data-source names.
