import heapq

class Cluster:

    def __init__(self, word):
        self.word = word

    def __str__(self):
        return self.word

    def __repr__(self):
        return '(C: {0})'.format(self.word)



def quality(cluster):
    pass


def createClusters(mostFreq):
    clusters = []
    for word in mostFreq:
        clusters.append(Cluster(word))
    return clusters


def MaxQuality(clusters):
    c = clusters.pop(0)
    c1 = clusters.pop(0)
    clusters.append(Cluster('{0} {1}'.format(c.word,c1.word)))


def brownAlg(m, max_heap):

    mostFreq = max_heap[:m]

    clusters = createClusters(mostFreq)
    for i in range(m, len(max_heap)):
        clusters.append(Cluster(max_heap[i]))

        # should edit the cluster to contain one less cluster because it would have merged it
        MaxQuality(clusters)





def main():
    listForTree = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    heapq._heapify_max(listForTree)        # for a maxheap!!
    brownAlg(3, listForTree)


if __name__ == '__main__':
    main()

