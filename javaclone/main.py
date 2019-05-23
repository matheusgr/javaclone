import javaclone
import similarity


def main():
    contents = javaclone.process()
    items = contents.items()
    simi = similarity.sim_pairs(items)
    simi.sort(key=lambda x: x[2])
    for x, y, z in simi:
        print(x[:40] + ' ' + y[:40] + ' ' + str(z))

if __name__ == "__main__":
    main()
