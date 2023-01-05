from threading import Thread


class CLIDaemon(Thread):

    def __init__(self, print_queue):
        super().__init__()
        self.print_queue = print_queue
        self.print_func = None

    def run(self) -> None:
        while True:
            user_in = input("Enter the name of the card to print: ")
            print_func = self.print_func
            if print_func is None:
                print("Select a deck first!")
                continue
            try:
                print_func(self.print_queue, user_in)
            except Exception as e:
                print(e)
                print("No card found for this name!")
