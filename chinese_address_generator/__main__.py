from chinese_address_generator import generator
import platform

if __name__ == "__main__":
    print(platform.system())
    print(generator.generatelevel1())
    print(generator.generatelevel2())
    print(generator.generatelevel3())
    print(generator.generatelevel4())

