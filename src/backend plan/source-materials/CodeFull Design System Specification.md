# CodeFull Design System Specification

**Doc ID:** DS-001 | **Version:** 0.1 draft | **Status:** for design and frontend review | **Owner:** Design lead + Frontend lead **Upstream:** PRD-001 sec 11, SRS-001 (NFR-019, NFR-021, FR-PLT-009), the CodeFull logo, interactive prototype | **Downstream:** shared theme package, component library, Playbook steps PB-10 and PB-18, GAP-005 and GAP-010

## 1. Principles

1. **Clear and calm:** a dark-first, high-contrast interface with a white light theme; blue is the brand voice, navy and near-black give depth.
2. **Privacy is visible:** wherever data is shown to others, the interface says who can see it (public, anonymous, only you).
3. **Four numbers, four names:** XP, points, competition score, and reputation always carry distinct labels and styling (ECO-001 sec 2).
4. **Accessible by default:** WCAG 2.2 AA is the floor; contrast is tested on tokens, not on screens.
5. **Every state designed:** loading, empty, and error states exist for every data view (TC-1405).
6. **Tokens, not hex values:** components consume tokens only (cursorrules.md sec 11).

## 2. Logo and Brand

The CodeFull mark is a left bracket in bright blue and a right bracket in near-black navy, joined by a stylized F. The wordmark uses an F in blue and the rest in navy.

| Rule | Guidance |
| --- | --- |
| Clear space | At least the height of the F stem on all sides |
| Minimum size | Mark 24 px wide on screens (smaller loses the F counter); wordmark 96 px wide |
| Backgrounds | Full-color mark on white or light surfaces; on dark surfaces use a white or light-blue knockout version of the dark half so it stays legible (to be supplied by the designer as an SVG) |
| Do not | Stretch, rotate, recolor outside the palette, add effects, or place on busy imagery |
| Formats | Master SVG for the mark and wordmark, plus favicon, app icon, and social image exports; the pixel image used in the prototype is replaced by SVG |

The logo palette sampled from the supplied mark: bright blue near #2878E7 to #1D6BDB, mid blue near #1551B6, navy near #0F1E35.

## 3. Color Tokens

### 3.1 Brand and surface tokens

| Token | Dark theme | Light theme | Use |
| --- | --- | --- | --- |
| --bg | #0C0D10 | #F2F3F8 | Page background |
| --surface | #13151C | #FFFFFF | Cards, panels |
| --surface2 | #1A1D28 | #F0F2FA | Inputs, hover |
| --surface3 | #20243A | #E8EAFC | Raised elements |
| --border | #252A3D | #DDE0F0 | Decorative dividers |
| --control-border | #4A5580 (verify 3:1) | #7B86B3 (verify 3:1) | Input and control outlines |
| --text | #E8EAF4 | #1A1D2E | Primary text |
| --text2 | #A0A8C8 | #4A5080 | Secondary text |
| --text3 | #8A98C4 (proposed) | #5F6A98 (proposed) | Tertiary text and captions |
| --accent (navy) | #14315C | #14315C | Brand navy, headers, emphasis |
| --blue | #1D6BDB | #1D6BDB | Primary buttons, links on light |
| --blue-text-dark | #5B9BF0 (proposed) | n/a | Links and blue text on dark surfaces |
| --accent2 | #2878E7 | #2878E7 | Large graphics, icons, progress fills |
| --focus | #5B9BF0 | #1D6BDB | Focus ring (2 px with 2 px offset) |

### 3.2 Semantic tokens

| Token | Dark | Light | Use |
| --- | --- | --- | --- |
| --success | #22C55E (text and icons) | #15803D | Success, wins |
| --success-bg | #15803D with white text | #15803D with white text | Success buttons and badges |
| --danger | #F87171 (text on dark) | #B91C1C | Errors, destructive actions |
| --danger-bg | #B91C1C with white text | #B91C1C with white text | Destructive buttons |
| --warning | #F59E0B (text on dark) | #92400E | Cautions |
| --live | #C2410C with white text | #C2410C with white text | Live badges and orange buttons |
| --ai | #8B7FD6 (violet) | #5B50B0 | Reserved for AI-touched UI only; confirm against brand rules |

Gold, silver, and bronze tones are used only for podium ranks.

### 3.3 Contrast verification (computed)

Contrast ratios were computed from the hex values (WCAG relative luminance). Normal text needs 4.5:1, large text and meaningful graphics 3:1.

| Pair | Ratio | Result |
| --- | --- | --- |
| Dark: --text on --surface | 15.2 | Pass |
| Dark: --text2 on --surface | 7.8 | Pass |
| Dark: current text3 #6070A0 on --surface | 3.75 | Fail for small text; replace |
| Dark: proposed text3 #8A98C4 on --surface | 6.4 | Pass |
| Dark: #2878E7 as text on --surface | 4.28 | Fail for small text; use --blue-text-dark |
| Dark: #5B9BF0 on --surface | 6.4 | Pass |
| Light: --text on white | 16.7 | Pass |
| Light: --text2 on white | 7.6 | Pass |
| Light: current text3 #8890B8 on white | 3.12 | Fail; replace |
| Light: proposed text3 #5F6A98 on white | 5.25 | Pass |
| White on --blue #1D6BDB (primary button) | 5.03 | Pass |
| White on #2878E7 | 4.26 | Fail for normal text; use --blue for button fills |
| White on navy #14315C | 12.9 | Pass |
| Light: --blue on white (links) | 5.03 | Pass |
| White on #E8630A (orange button) | 3.38 | Fail; use #C2410C (5.18) |
| White on #22C55E (green button) | 2.28 | Fail; use #15803D (5.02) |
| Light: #22C55E text on white | 2.28 | Fail; use #15803D |
| Light: #EF4444 text on white | 3.76 | Fail; use #B91C1C (6.47) |
| Dark: AI violet #8B7FD6 on --surface | 5.3 | Pass |
| Light: AI violet #5B50B0 on white | 6.5 | Pass |

These results confirm GAP-005: several prototype colors fall below AA and are replaced by the tokens above. A token test in CI computes the ratio for every foreground and background pairing and fails below the threshold. Control outlines (inputs, checkboxes) must reach 3:1 against their background; the proposed values are to be verified by that test.

## 4. Typography

| Role | Font | Notes |
| --- | --- | --- |
| Display and headings | Space Grotesk 600 and 700 | Tight tracking for large sizes |
| Body and UI | IBM Plex Sans 400, 500, 600 |  |
| Code and numbers in tables | IBM Plex Mono 400, 500 | Tabular figures for scores and times |

Fonts are self-hosted with font-display: swap and metric-compatible fallbacks to avoid layout shift (NFR-005).

| Style | Size / line height | Weight |
| --- | --- | --- |
| Display | 36 / 44 (28 / 36 on mobile) | 700 |
| H1 | 24 / 32 | 700 |
| H2 | 18 / 26 | 600 |
| H3 | 16 / 24 | 600 |
| Body | 14 / 22 | 400 |
| Small | 12 / 18 | 400 or 500 |
| Caption | 11 / 16 | 500; never below 11 px |
| Code | 12.5 / 22 | 400 |

User text scales with browser zoom up to 200% without loss of content or function.

## 5. Layout, Spacing, Shape, Motion

| Topic | Specification |
| --- | --- |
| Breakpoints | 320 (minimum), 375, 768, 860 (sidebar becomes a drawer, as in the prototype), 1024, 1440 |
| Spacing scale | 4, 8, 12, 16, 20, 24, 32, 48 px |
| Radius | 8 px controls, 10 to 14 px cards, 999 px chips and pills |
| Elevation | Border first; shadow only for overlays (modals, menus, toasts) |
| Content width | Page content max 1200 px; reading text max 72 characters |
| Motion | 120 to 200 ms ease-out for state changes; respect prefers-reduced-motion by removing non-essential animation (live pulse, shimmer) |

## 6. Component Inventory

Each component ships with documented states (default, hover, focus, active, disabled, loading, error) and keyboard behavior.

| Group | Components |
| --- | --- |
| Actions | Button (primary, secondary, ghost, destructive, live), icon button, link |
| Inputs | Text field, textarea, select, checkbox, radio, toggle, segmented control, tag input; all with visible labels, help and error text |
| Navigation | Header with search, sidebar with groups and badges, drawer, tabs, breadcrumbs, pagination or load more |
| Data display | Card, stat card, table with sticky header and horizontal scroll container, list item, progress bar, tier chip, badge, avatar, achievement tile, heatmap, code block |
| Feedback | Toast, banner, modal and confirm dialog, tooltip, skeleton loader, empty state, error state with retry |
| Domain components | Leaderboard row (with Anonymous and lock indicator, rank change), podium, challenge card, battle scoreboard, lesson player with format switcher, playground (code editor, output pane, limits notice), tutor chat (AI accent), question card (open or discreet indicator), points and XP panel, plan comparison card, privacy indicator |

### Privacy indicator

A small, consistent control shown wherever user content or identity can be seen by others: Public, Anonymous, Only you, Only you and mentor. It includes an accessible name and links to the setting.

### Four-number panel

XP uses the tier progress bar; points use a coin icon with learning and prize bucket detail on demand; competition score uses a rank icon; reputation uses a star. Labels are always present; color never carries meaning alone.

## 7. State Patterns

| State | Pattern |
| --- | --- |
| Loading | Skeletons matching the final layout; spinners only for short actions; announce loading to assistive technology |
| Empty | Illustration or icon, one sentence on why it is empty, one primary action |
| Error | Plain-language message, what the user can do, retry action, request id for support; never raw errors |
| Offline (desktop and mobile) | Banner with queued changes count; actions that need the server are disabled with an explanation |
| Quota or limit reached | Show usage, the plan limit, and the upgrade path (UAT-015, UAT-036) |
| Moderation or hold | Explain that an action is under review without exposing internal signals |

## 8. Accessibility Requirements (NFR-019)

- Every interactive element is a real button, link, or form control with an accessible name; no clickable divs.
- Visible focus on all controls using --focus; logical tab order; skip link to main content; no keyboard traps; drawers and modals trap focus correctly and restore it on close.
- Do not rely on color alone for status, rank change, wins and losses, or privacy state; pair with icon and text.
- Live regions announce toasts, run results, and scoreboard changes at a sensible rate.
- Code editor: keyboard accessible, with a documented way to leave the editor and screen reader support.
- Targets at least 24 by 24 px, 44 px on touch; text spacing and zoom tolerant layouts.
- Test with axe in CI, manual screen reader passes each release, and the contrast test on tokens (TC-1401, TC-1402, TC-1406).

## 9. Theming and Implementation

| Topic | Specification |
| --- | --- |
| Tokens source | A single tokens.json (design tokens format) generating CSS custom properties, TypeScript constants, and the Tailwind theme |
| Themes | :root holds light values; \[data-theme=dark\] overrides; prefers-color-scheme sets the default when the user has not chosen; the choice is persisted (FR-PLT-009) |
| Package | packages/ui in the monorepo: tokens, components, icons, and docs; consumed by web, desktop shell, and mobile shell where applicable |
| Documentation | Storybook with every state and an accessibility panel; visual regression on pull requests |
| Icons | One SVG icon set (for example Lucide); emoji in the prototype are replaced because they render differently per platform and are not accessible by default |
| Code editor | A maintained editor component (for example CodeMirror or Monaco) themed with the tokens |
| Charts | Accessible chart components with text alternatives and patterns, not color alone |
| Imagery | Illustrations in the brand palette; no stock imagery implying outcomes or earnings |

## 10. Content and Microcopy Guidelines

- Plain, friendly, and direct; no hype about earnings or guaranteed outcomes.
- Always say who can see something: for example Visible to everyone, Shown as Anonymous, Only you can see this.
- Never call XP or competition score points. Do not promise cash value for points before Phase 2 and Legal approval.
- Errors explain what happened and what to do next.
- Dates, times, and numbers follow the user locale; strings are externalized (NFR-026, TC-1317).

## 11. Prototype Migration Map

| Prototype element | Production component or token |
| --- | --- |
| .btn-primary, .btn-orange, .btn-green | Button primary (--blue), live (#C2410C), success (#15803D) |
| .card, .stat-card | Card, StatCard |
| .tier-chip, .badge | TierChip, Badge with icon and text |
| .progress-bar | ProgressBar with accessible value |
| Toggle divs with inline handlers | Toggle (real switch role) |
| .tab-row, .tab-btn | Tabs with roles and arrow-key navigation |
| Leaderboard and podium markup | LeaderboardRow, Podium with Anonymous indicator |
| contenteditable editor | Code editor component |
| Inline colors in templates | Token references |
| Emoji icons | Icon set |
| Static text such as 128K+ coders | Removed until real data exists (GAP-009) |

## 12. Open Items

- Provide the logo master SVGs, including the light-on-dark version of the dark half of the mark.
- Confirm the AI accent (violet) or choose a blue-family alternative (GAP-010).
- Verify the proposed text3 and control-border values with the token contrast test.
- Choose the icon set and the code editor component.
- Decide dark-first or system default for first-time visitors.
