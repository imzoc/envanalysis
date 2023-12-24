consonants = ["p", "b", 'f', 'v', '1', 'w', 'θ', 'ð', 't', 'd', 's', 'z', 'n', 'l', 'ɹ', 'ʃ', 'ʒ', 't͡ʃ', 'd͡ʒ', 'j', 'k', 'g', 'ŋ', 'h']
clusters = []
for c1 in consonants:
    for c2 in consonants:
        for c3 in consonants:
            if (c1 != c2 and c2 != c3) and True:
                clusters.append(c1 + c2 + c3)

print(clusters)
print(len(clusters))