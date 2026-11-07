/* ODIN V11.5 – Einfacher Einstieg statt zusätzlicher Menüs. */
const odinV115PreviousPlay = playView;
const odinV115PreviousFunds = fundsView;
const odinV115PreviousMission = odinMission;
function odinV115NextStep() {
  const fund = chosenFund(state);
  if (!fund) return 'Gründe deinen ersten Fonds und starte dein Imperium.';
  const talks = availableTalks(state);
  const reviews = availableReviews(state);
  if (fund.fundraise && fund.commitmentTotal === 0 && talks > 0)
    return 'Starte mit einem Anlegergespräch. Mit einer Zusage kannst du investieren.';
  if (fund.fundraise && talks > 0 && fund.commitmentTotal < fund.target * .5)
    return 'Sprich mit Anlegern, um Kapital für neue Investments zu sichern.';
  if (reviews > 0 && fund.commitmentTotal > 0)
    return 'Prüfe ein Zielfondsangebot und entscheide über dein nächstes Investment.';
  if (reviews > 0 && !fund.commitmentTotal)
    return 'Noch kein Anlegerkapital vorhanden? Nutze den nächsten Monat für Fundraising.';
  if (talks > 0)
    return 'Ein Anlegergespräch ist möglich. Oder du startest den nächsten Monat.';
  return 'Für diesen Monat ist alles erledigt. Weiter geht es im nächsten Monat!';
}
playView = function() {
  const html = odinV115PreviousPlay();
  if (!state.funds.length || launchMode || state.win || state.loss) return html;
  return html.replace('Ein gutes Urteil. Ein großer Fonds. Oder eine ziemlich teure Pointe.',
                      esc(odinV115NextStep()));
};
fundsView = function() {
  return odinV115PreviousFunds()
    .replace('💶 25 % LP-Kapital abrufen', '💶 25 % Anlegerkapital abrufen')
    .replace('💸 Ausschütten', '💸 An Anleger auszahlen');
};
odinMission = function() {
  if (state.funds.length &&
      state.funds.some(f => f.commitmentTotal > 0) &&
      state.funds.some(f => f.holdings.length > 0) && state.month >= 3)
    return '';
  return odinV115PreviousMission();
};
const odinV115Style = document.createElement('style');
odinV115Style.textContent = [
  '',
  '/* Bessere Lesbarkeit der nächsten Aktion auf kleinen Displays. */',
  '.decision-head p {max-width:42ch;line-height:1.5}',
  '@media(max-width:560px){',
  ' .decision-head p{font-size:13px;margin:6px 0 0;color:#e1e9e3}',
  ' .choice-tabs button{min-height:46px}',
  ' .fund-choice{min-height:52px}',
  ' .btn:focus-visible,.choice-tabs button:focus-visible,.fund-choice:focus-visible{outline:3px solid #ffe4a7;outline-offset:3px}',
  '}',
  '@media(prefers-reduced-motion:reduce){.odin-payout-alert,.mission-board{animation:none!important;transition:none!important}}',
  ''
].join("\n");
document.head.appendChild(odinV115Style);
document.title = 'Private Markets Tycoon V11.5 – Nightly Evolution';
const odinV115Brand = document.querySelector('.brand small');
if (odinV115Brand) odinV115Brand.textContent = 'V11.5 · NIGHTLY EVOLUTION';
