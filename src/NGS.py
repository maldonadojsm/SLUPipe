import Controller
import config as cfg
def main():
    NGS = Controller.Controller(cfg.configuration)
    NGS.run()


if __name__ == '__main__':
    main()


