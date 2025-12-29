import queue
import threading

from listener import ListenerAgent
from secretary import SecretaryAgent
from ui import ContextOverlay


def main():
    # Communication Queue
    text_queue = queue.Queue()

    # UI needs to be created in main thread
    # We define a wrapper for the secretary callback to update UI safely

    def on_bullets_update(bullets):
        # Schedule update on main thread
        app.after(0, lambda: app.update_bullets(bullets))

    def on_clear_requested():
        print("Clearing context...")
        secretary.clear()
        # Optionally wait for new input or just reset

    # Initialize UI
    app = ContextOverlay(clear_callback=on_clear_requested)

    # Initialize Agents
    # Note: Listener needs 'small' model.
    listener = ListenerAgent(output_queue=text_queue, model_size="small")
    secretary = SecretaryAgent(input_queue=text_queue, update_callback=on_bullets_update)

    # Start Agents
    listener.start()
    secretary.start()

    # Run UI Loop
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping agents...")
        listener.stop()
        secretary.stop()
        print("Exited.")


if __name__ == "__main__":
    main()
