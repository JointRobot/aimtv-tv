# AIMTV live desk: style guide for the hourly refresh

AIMTV is a television channel from **Earth 69**, city **Bombai, Hindia** (formerly India), in the year **2041**. We broadcast from 15 years in the future, so real-world news from today is "old news" that "fifteen years ago, it was 2026". Everything is satire seen from 2041. Never present invented events as real. Real events are named plainly and kindly; the jokes land on gadgets, corporations, habits and the future, never on real private people, victims, religion, caste or communities. No tragedies as punchlines (disasters, deaths, wars: state them gravely and briefly or skip them).

## Voice rules (founder)
- Predominantly English. Regional language only for a hello or a goodbye (Namaste, Namaskara, Jhulelal, Kem cho, Sat Sri Akal) and sound effects.
- Urban Indian audience. Plain, witty, short lines. Each spoken line is one or two short sentences, at most about 25 words (hard limit 260 characters). Say numbers and dates in words where natural ("the fifth of October").
- No links, hashtags or emoji in speech. Use real spellings in text; pronunciation hints are applied automatically.
- Sponsors are fictional (Fa Corp, Fa Cough Syrup and so on). Never name a real brand as a sponsor or imply endorsement.

## Characters and speakers (use these ids as the first item of each line)
- `hema`: Hema, journalist by day (Malini by night; never mention that). Anchors **This Day, That Year** (`tdty`): crisp, deadpan, fact first, then a dry take. Sign-on: "Namaste, I'm Hema. You're watching This Day, That Year." Sign-off: "That's the record. Everything else is just a take. I'm Hema. Namaste, see you at the next bulletin." (the desk refreshes hourly, never say "tomorrow")
- `tchu`: Tchu Tchu, taxi driver (Premier Padmini), Bangalore-born, two dogs (Dalmatian, "something is fishy with the Dalmatian"; Animation). Catchphrases: "Who notices a notice?", "Work is warship.", "The meter is still running." Hosts **Meter Down** (`meter`), live from the taxi, reacting to the day's news from street level, in Shivajinagar.
- `jc`: Juhu Chaiwala (JC), spy with chai. Chai Rs 12 at the shadow entrance, Rs 900 at the sunny entrance. Hosts **Tomorrow Shop** (`shop`): a "product from the future" each time, with a twist about class or tech. `chaibot` is his samovar robot: one-liners ("And fast too." "Here is your chai. From a bot.").
- `sarla`: Stomach Challo, American-accent travel vlogger who has never left West India ("I love foreign"). Hosts **Stomach Challo Travels** (`travel`): a nearby place presented as a foreign trip.
- `fadarr`: Fa Darr, ex-priest, CEO of Fa Corporation. Voices the sponsor spots (`ad1`): fictional products (Fa Cough Syrup, Fa Cars, Fa King Construction, Fa Call Centre), absurd side effects ("Side effects may include eviction."). Villain, but a comic one.
- `mrst`: Sindhi Crawford (Mrs Takechandani), Road Cross NGO since 2008. Road-safety PSA (`psa`): "Don't take tension. We help you cross."
- `baba`: Almighty Baba Black Sheep, the daily blessing (`baba`): says only "Baa" lines and one short blessing. Keep to 2 to 3 lines.
- Others who can speak if needed: `lata` (Bhenji Jumping, Gujarati aunty, skateboard and dosas), `devi` (Fullon Devi, stunt woman), `animation` (Marathi dog who jumps between media).
- World facts: Fa King Construction is Fa Corp's demolition arm and keeps posting eviction notices at Celeb Shauchalay, the last chawl, in Shivajinagar. Project Unearth is "unlimited space in space". Fame Meter: "No publicity, no action."

## Programme formats (lines per bulletin; keep each programme 5 to 8 lines unless stated)
- `tdty` (This Day, That Year), 8 lines: sign-on; "Today's date is the <day> of <month>. And fifteen years ago, it was 2026."; three or four items from today's real news (one line each, as "Old news.", "Vintage gadget.", "Ancient media." style tags, then the fact, then a dry 2041 take); a closing take; the sign-off. Keep facts accurate and sourced from today's headlines. Stamp: `Archived · <d> <Mon> 2026`.
- `meter` (Meter Down), 5 lines: "Namaskara! Meter down. Tchu Tchu reporting, live from the taxi."; two street-level reactions to the same news (a fare, a traffic jam, a poster, the Dalmatian); one eviction-notice or Fa King beat; the sign-off "Tchu Tchu, AIMTV, Bombai. The meter is still running." Stamp: `Live · Shivajinagar`.
- `shop` (6 to 8 lines): a new product from 2041, price in rupees, shadow price vs sunny price joke, ends with Chaibot.
- `travel` (5 to 6 lines): Sarla's trip to a nearby place described as abroad.
- `ad1` (4 lines): one fictional Fa Corp product.
- `psa` (3 lines): one road-safety tip, tied to weather or news where relevant.
- `baba` (2 to 3 lines).

## Ticker
8 to 12 items, short, upper case. Mix: one dated line ("ARCHIVED: 5 OCTOBER 2026"), real headline fragments from today (neutral wording), and canon gags (Fa King demolition, chai prices, Road Cross, Fame Meter). Max about 90 characters each.

## Continuity
Read `site/live/live.json` before writing: do not repeat last hour's items or jokes; carry running gags forward (for example a poster Tchu Tchu keeps noticing) so the channel feels like one ongoing story.
