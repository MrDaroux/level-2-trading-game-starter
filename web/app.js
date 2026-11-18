// SUPPLIED browser plumbing. No game rules or student input validation here.
const form = document.querySelector('#controls');
const inputs = document.querySelector('#inputs');
const output = document.querySelector('#output');
const status = document.querySelector('#status');
let busy = false;
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (busy) return;
  const action = event.submitter?.value;
  if (!action) return;
  const fields = Object.fromEntries(new FormData(form).entries());
  busy = true;
  inputs.disabled = true;
  status.textContent = 'Waiting for Python…';
  try {
    const response = await fetch('/action', {
      method: 'POST',
      headers: {'Content-Type': 'application/json',
        'X-Request-Token': document.querySelector('meta[name="request-token"]').content},
      body: JSON.stringify({action, fields})
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'The server could not complete this action.');
    // Display text, never interpret student/player content as HTML.
    output.textContent = result.text;
    status.textContent = 'Python response displayed.';
  } catch (error) {
    status.textContent = `Connection or program error: ${error.message} ` +
      'Check the terminal and game state before trying again. No automatic retry was made.';
  } finally {
    busy = false;
    inputs.disabled = false;
  }
});
