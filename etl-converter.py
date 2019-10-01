import pandas
import matplotlib.pyplot as plt

names = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'class']
dataset = pandas.read_csv('data/crx.csv', names=names)


def map_value(value, old, new):
    for k, v in enumerate(old):
        if value == v:
            return new[k]
    return value


# shape
print(dataset.shape)

# head
print(dataset.head(20))

# class distribution
print(dataset.groupby('class').size())

# box and whisker plots
# dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
# plt.show()

result = []

for row in dataset.values:
    # print(row)
    row[3] = map_value(row[3], ('u', 'y', 'l', 't'), ('a', 'b', 'c', 'd'))
    row[4] = map_value(row[4], ('g', 'p', 'gg'), ('a', 'b', 'c'))
    row[5] = map_value(row[5], ('c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff'),
                       ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'))
    row[6] = map_value(row[6], ('v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o'),
                       ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'))
    row[8] = map_value(row[8], ('t', 'f'), ('a', 'b'))
    row[9] = map_value(row[9], ('t', 'f'), ('a', 'b'))
    row[11] = map_value(row[11], ('t', 'f'), ('a', 'b'))
    row[12] = map_value(row[12], ('g', 'p', 's'), ('a', 'b', 'c'))

    print
    result.append(row.tolist())

df = pandas.DataFrame(result, columns=names)

print(df.head(20))

df.to_csv(header=False, path_or_buf='output.csv')
