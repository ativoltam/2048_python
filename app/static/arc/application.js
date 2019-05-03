// Wait till the browser is ready to render the game (avoids glitches)
// window.requestAnimationFrame(), tells the browser to perform
// an animation, take a callback as an arg to invoke before repaint
window.requestAnimationFrame(function () { /
  new GameManager(4, KeyboardInputManager, HTMLActuator, LocalStorageManager);
});
