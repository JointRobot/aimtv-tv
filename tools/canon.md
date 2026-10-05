# AIMTV live desk: style guide for the live refresh (every two hours)

AIMTV is a television channel from **Earth 69**, city **Bombai, Hindia** (formerly India), in the year **2041**. We broadcast from 15 years in the future, so real-world news from today is "old news" that "fifteen years ago, it was 2026". Everything is satire seen from 2041. Never present invented events as real. Real events are named plainly and kindly; the jokes land on gadgets, corporations, habits and the future, never on real private people, victims, religion, caste or communities. No tragedies as punchlines (disasters, deaths, wars: state them gravely and briefly or skip them).

## Voice rules (founder)
- Predominantly English. Regional language only for a hello or a goodbye (Namaste, Namaskara, Jhulelal, Kem cho, Sat Sri Akal) and sound effects.
- Urban Indian audience. Plain, witty, short lines. Each spoken line is one or two short sentences, at most about 25 words (hard limit 260 characters). Say numbers and dates in words where natural ("the fifth of October").
- No links, hashtags or emoji in speech. Use real spellings in text; pronunciation hints are applied automatically.
- Sponsors are fictional (Fa Corp, Fa Cough Syrup and so on). Never name a real brand as a sponsor or imply endorsement.

## Characters and speakers (use these ids as the first item of each line)
- `hema`: Hema, journalist by day (Malini by night; never mention that). Anchors **This Day, That Year** (`tdty`). She is a serious, BBC-calibre anchor: the biggest world and India stories of the day (politics, protests, diplomacy, economy, courts, climate, science). Fact first, gravely and precisely, then a calm 2041 look back at what that moment led to (a law, an institution, a habit, a technology of 2041). No tech or gadget jokes from Hema: those belong to JC. Sign-on: "Namaste, I'm Hema. You're watching This Day, That Year." Sign-off: "That's the record. Everything else is just a take. I'm Hema. Namaste, see you at the next bulletin." (the desk refreshes every two hours, never say "tomorrow")
- `tchu`: Tchu Tchu, taxi driver (Premier Padmini), Bangalore-born, two dogs (Dalmatian, "something is fishy with the Dalmatian"; Animation). Catchphrases: "Who notices a notice?", "Work is warship.", "The meter is still running." Hosts **Meter Down** (`meter`), live from the taxi, reacting to the day's news from street level, in Shivajinagar.
- `jc`: Juhu Chaiwala (JC), spy with chai. Chai Rs 12 at the shadow entrance, Rs 900 at the sunny entrance. Hosts **Tomorrow Shop** (`shop`) and owns the tech beat: the day's real tech, AI, gadget, startup and internet news, each turned into the 2041 product it became, with a twist about class or tech. `chaibot` is his samovar robot: one-liners ("And fast too." "Here is your chai. From a bot.").
- `sarla`: Stomach Challo, American-accent travel vlogger who has never left West India ("I love foreign"). Hosts **Stomach Challo Travels** (`travel`): a nearby place presented as a foreign trip.
- `fadarr`: Fa Darr, ex-priest, CEO of Fa Corporation. Voices the sponsor spots (`ad1`): fictional products (Fa Cough Syrup, Fa Cars, Fa King Construction, Fa Call Centre), absurd side effects ("Side effects may include eviction."). Villain, but a comic one.
- `mrst`: Sindhi Crawford (Mrs Takechandani), Road Cross NGO since 2008. Road-safety PSA (`psa`): "Don't take tension. We help you cross."
- `baba`: Almighty Baba Black Sheep, the daily blessing (`baba`): speaks only "Baa" lines; the English subtitle carries one short blessing. Keep to 2 to 3 lines. Founder's lines to reuse: "You are either photogenic or sarvajnic."
- Others who can speak if needed: `lata` (Bhenji Jumping, Gujarati aunty, skateboard and dosas), `devi` (Fullon Devi, stunt woman), `animation` (Marathi dog who jumps between media).
- World facts: Fa King Construction is Fa Corp's demolition arm and keeps posting eviction notices at Celeb Shauchalay, the last chawl, in Shivajinagar. Project Unearth is "unlimited space in space". Fame Meter: "No publicity, no action."

## Looking back from 2041 (the house angle)
Every story is told as history: today is "fifteen years ago". The take asks what this moment turned into by 2041: the institution, rule, product or habit it led to. Point the satire at power, systems, corporations and gadgets.
Hard limit: stories of violence, lynching, riots, deaths, disasters or communal or religious conflict are reported straight and briefly by Hema (or skipped), with no joke, no invented product and no 2041 gag. Satire on such topics is only made in hand-written episodes the founder approves, never by the automatic desk.

## Regional line (every spoken line)
Each line has a fourth field: the same line translated into the speaker's home language, in its own script. It shows in yellow under the English subtitle. Keep it natural and short; names stay as names.
Languages: hema, jc, chaibot, baba: Hindi (Devanagari). tchu: Kannada. animation: Marathi. sarla, lata: Gujarati. dimpy, devi: Punjabi (Gurmukhi). mrst: Sindhi (Devanagari). fadarr: Malayalam. gutter: Tamil. arnold: Konkani (Devanagari). tabla: Assamese.
The third field (English language note) is optional and usually empty.

## Programme formats (lines per bulletin; keep each programme 5 to 8 lines unless stated)
- `tdty` (This Day, That Year), 8 lines: sign-on; "Today's date is the <day> of <month>. And fifteen years ago, it was 2026."; three or four of the day's biggest world and India stories (one line each, tagged "Old news." or "From the archive.", then the fact, then what it led to by 2041; no gadget items, those go to JC); a closing take; the sign-off. Keep facts accurate and sourced from today's headlines. Stamp: `Archived · <d> <Mon> 2026`.
- `meter` (Meter Down), 5 lines: "Namaskara! Meter down. Tchu Tchu reporting, live from the taxi."; two street-level reactions to the same news (a fare, a traffic jam, a poster, the Dalmatian); one eviction-notice or Fa King beat; the sign-off "Tchu Tchu, AIMTV, Bombai. The meter is still running." Stamp: `Live · Shivajinagar`.
- `shop` (6 to 8 lines, refreshed every run): JC takes one or two real tech stories of the day and shows the 2041 product each became; price in rupees, shadow price vs sunny price joke, ends with Chaibot. Stamp: `Tech desk · <d> <Mon> 2026`.
- `travel` (5 to 6 lines): Sarla's trip to a nearby place described as abroad.
- `ad1` (4 lines): one fictional Fa Corp product.
- `psa` (3 lines): one road-safety tip, tied to weather or news where relevant.
- `baba` (2 to 3 lines).

## Ticker
8 to 12 items, short, upper case. Mix: one dated line ("ARCHIVED: 5 OCTOBER 2026"), real headline fragments from today (neutral wording), and canon gags (Fa King demolition, chai prices, Road Cross, Fame Meter). Max about 90 characters each.

## Continuity
Read `site/live/live.json` before writing: do not repeat the last bulletin's items or jokes; carry running gags forward (for example a poster Tchu Tchu keeps noticing) so the channel feels like one ongoing story.
