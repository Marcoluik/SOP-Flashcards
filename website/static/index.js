function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteFlashcard(cardId) {
  console.log("Script loaded.");
  fetch("/delete-card", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ cardId: cardId }),
  }).then((_res) => {
    location.reload();
  });
}
