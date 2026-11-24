# Design System

## Style
Clinical, calm, trustworthy, uncluttered. Looks like a healthcare product, not a startup landing page.

## Color Palette (medical teal–blue)
| Token | Hex | Use |
|---|---|---|
| --primary-700 | #0B5E75 | Headers, primary buttons (hover) |
| --primary-600 | #0F7A8C | Primary buttons, links |
| --primary-100 | #E1F1F4 | Soft highlights, selected tabs |
| --bg | #F4F8FA | Page background |
| --surface | #FFFFFF | Cards, forms |
| --text | #1B2B34 | Body text |
| --muted | #5B6F7A | Helper text |
| --border | #D5E1E7 | Inputs, dividers |
| --ok | #2E7D5B | Non-anemia result |
| --ok-bg | #E6F3EC | Non-anemia background |
| --alert | #B3402F | Anemia result |
| --alert-bg | #FBEAE7 | Anemia background |

## Gradient (single, restrained, clinical)
Used ONLY on the top bar and the auth-page side panel:
```css
background: linear-gradient(135deg, #0B5E75 0%, #0F7A8C 100%);
```
Rules:
- Two close teal-blue tones, same hue family, no rainbow.
- NO purple, pink, neon, mesh or glowing gradients.
- NO gradients on cards, text or result badges.
- Result badges use flat green / red.

## Typography
- Font: **Source Sans 3** (fallback: system-ui, Segoe UI, Arial). Self-host or system fallback; no tracking scripts.
- Scale: 14 / 16 / 18 / 24 / 32 px.
- Weights: 400 body, 600 headings and buttons.
- Sentence case everywhere. No all-caps labels.
- Line length under 75 characters.

## Layout
### Auth page
```
+---------------------+------------------------+
|  gradient panel     |  [Login | Register]    |
|  logo + 1 sentence  |  email                 |
|  what the app does  |  password              |
|                     |  [Sign in]             |
+---------------------+------------------------+
```
### Dashboard
```
+------------------------------------------------+
| AnemiaScan                    Hi, Priya [Logout]|
+---------------------------+--------------------+
| New scan                  | Result             |
| Name / Age / Place        | Status badge       |
| [Upload image + preview]  | Hb value g/dL      |
| [Analyse image]           | [Print report]     |
+---------------------------+--------------------+
| Your previous reports (table)                  |
+------------------------------------------------+
```
Left-aligned content. Max content width 1100px.

## Components
- **Buttons:** Primary (solid teal), Secondary (outline), Destructive (solid red, confirm dialog).
- **Cards:** radius 8px, 1px border, no heavy shadow.
- **Inputs:** 44px height, visible label above, error text below in --alert.
- **Upload zone:** dashed border, shows thumbnail after selection, file name and size.
- **Result badge:** flat colour, icon + text (never colour alone).
- **Table:** zebra rows, Print / Delete actions.

## Copy Guidelines
- Buttons: "Sign in", "Create account", "Analyse image", "Print report", "Delete report".
- Errors say what is wrong and how to fix it: "Image must be PNG or JPG and under 5 MB."
- Empty history: "No reports yet. Upload an image to run your first scan."
- Result texts: "Non-anemia" / "Anemia".

## UX Requirements
- Mobile responsive (375px, 768px, 1440px)
- Loading state on Analyse button ("Analysing…")
- Empty, error and success states
- Accessible forms: labels, aria-live for results, 4.5:1 contrast, visible focus ring
- Keyboard operable
- Respect prefers-reduced-motion; no decorative animation

## Print Stylesheet (print.css)
- Hide navbar, buttons and history.
- White background, black text, A4 portrait.
- Show: app name, report ID, date, patient name, age, place, image thumbnail, status, Hb value, reference note, disclaimer, footer.
- Status uses text + border, readable in black and white.

## Hb Reference Note (shown on report)
WHO anemia cut-offs: adult men below 13 g/dL, non-pregnant women below 12 g/dL, pregnant women below 11 g/dL, children 5–11 years below 11.5 g/dL, children 12–14 years below 12 g/dL.

## Remember
DESIGN.md = HOW IT SHOULD LOOK AND FEEL
