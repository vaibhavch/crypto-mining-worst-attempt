import csv
import datetime
import numpy
import os
import yaml

from nupic.algorithms.sdr_classifier_factory import SDRClassifierFactory
from nupic.algorithms.spatial_pooler import SpatialPooler
from nupic.algorithms.temporal_memory import TemporalMemory
from nupic.encoders.date import DateEncoder
from nupic.encoders.random_distributed_scalar import \
  RandomDistributedScalarEncoder 
from nupic.encoders.pass_through import PassThroughEncoder
import cPickle as pickle

_NUM_RECORDS = 37866
_EXAMPLE_DIR = os.path.dirname(os.path.abspath(__file__))
_INPUT_FILE_PATH = os.path.join(_EXAMPLE_DIR, "data", "cryptonight.csv")
_PARAMS_PATH = os.path.join(_EXAMPLE_DIR, "params", "model.yaml")


def getPredictionResults(network, clRegionName):
  """Get prediction results for all prediction steps."""
  classifierRegion = network.regions[clRegionName]
  actualValues = classifierRegion.getOutputData("actualValues")
  probabilities = classifierRegion.getOutputData("probabilities")
  steps = classifierRegion.getSelf().stepsList
  N = classifierRegion.getSelf().maxCategoryCount
  results = {step: {} for step in steps}
  for i in range(len(steps)):
    # stepProbabilities are probabilities for this prediction step only.
    stepProbabilities = probabilities[i * N:(i + 1) * N - 1]
    mostLikelyCategoryIdx = stepProbabilities.argmax()
    predictedValue = actualValues[mostLikelyCategoryIdx]
    predictionConfidence = stepProbabilities[mostLikelyCategoryIdx]
    results[steps[i]]["predictedValue"] = predictedValue
    results[steps[i]]["predictionConfidence"] = predictionConfidence
  return results



def runHotgym(numRecords):
  with open(_PARAMS_PATH, "r") as f:
    modelParams = yaml.safe_load(f)["modelParams"]
    enParams = modelParams["sensorParams"]["encoders"]
    spParams = modelParams["spParams"]
    tmParams = modelParams["tmParams"]

  scalarEncoder = RandomDistributedScalarEncoder(0.000000000001,w=49, seed=81, n=1023)
  encodingWidth = (scalarEncoder.getWidth() * 5)

  sp = SpatialPooler(
    inputDimensions=(encodingWidth,),
    columnDimensions=(spParams["columnCount"],),
    potentialPct=spParams["potentialPct"],
    potentialRadius=encodingWidth,
    globalInhibition=spParams["globalInhibition"],
    localAreaDensity=spParams["localAreaDensity"],
    numActiveColumnsPerInhArea=spParams["numActiveColumnsPerInhArea"],
    synPermInactiveDec=spParams["synPermInactiveDec"],
    synPermActiveInc=spParams["synPermActiveInc"],
    synPermConnected=spParams["synPermConnected"],
    boostStrength=spParams["boostStrength"],
    seed=spParams["seed"],
    wrapAround=True
  )
  '''
  tm = TemporalMemory(
    columnDimensions=(tmParams["columnCount"],),
    cellsPerColumn=tmParams["cellsPerColumn"],
    activationThreshold=tmParams["activationThreshold"],
    initialPermanence=tmParams["initialPerm"],
    connectedPermanence=spParams["synPermConnected"],
    minThreshold=tmParams["minThreshold"],
    maxNewSynapseCount=tmParams["newSynapseCount"],
    permanenceIncrement=tmParams["permanenceInc"],
    permanenceDecrement=tmParams["permanenceDec"],
    predictedSegmentDecrement=0.0,
    maxSegmentsPerCell=tmParams["maxSegmentsPerCell"],
    maxSynapsesPerSegment=tmParams["maxSynapsesPerSegment"],
    seed=tmParams["seed"]
  )
  '''
  classifier = SDRClassifierFactory.create()
  results = []
  with open(_INPUT_FILE_PATH, "r") as fin:
    reader = csv.reader(fin)
    headers = reader.next()
    reader.next()
    reader.next()

    for count, record in enumerate(reader):

      if count >= numRecords: break

      difficulty = long(record[0])
      prevhash = long(record[1])
      timestamp = long(record[2])
      txhash = long(record[3])
      nonce = int(int(record[4]))

      '''
      nonceBits = numpy.zeros(scalarEncoder.getWidth())
      difficultyBits = numpy.zeros(scalarEncoder.getWidth())
      prevhashBits = numpy.zeros(scalarEncoder.getWidth())
      timestampBits = numpy.zeros(scalarEncoder.getWidth())
      txhashBits = numpy.zeros(scalarEncoder.getWidth())
      '''

      difficultyBits = numpy.zeros(len(str(difficulty)))
      prevhashBits = numpy.zeros(len(str(prevhash)))
      timestampBits = numpy.zeros(len(str(timestamp)))
      txhashBits = numpy.zeros(len(str(txhash)))

      # Now we call the encoders to create bit representations for each value.
      scalarEncoder.encodeIntoArray(difficulty, difficultyBits)
      scalarEncoder.encodeIntoArray(prevhash, prevhashBits)
      scalarEncoder.encodeIntoArray(timestamp, timestampBits)
      scalarEncoder.encodeIntoArray(txhash, txhashBits)
      

      # Concatenate all these encodings into one large encoding for Spatial
      # Pooling.
      encoding = numpy.concatenate(
        [difficultyBits,prevhashBits,timestampBits,txhashBits]
      )
      
      print encoding.astype('int16')

      # Create an array to represent active columns, all initially zero. This
      # will be populated by the compute method below. It must have the same
      # dimensions as the Spatial Pooler.
      activeColumns = numpy.zeros(spParams["columnCount"])

      # Execute Spatial Pooling algorithm over input space.
      sp.compute(encoding, True, activeColumns)
      activeColumnIndices = numpy.nonzero(activeColumns)[0]

      # Execute Temporal Memory algorithm over active mini-columns.
      #tm.compute(activeColumnIndices, learn=True)

      #activeCells = tm.getActiveCells()

      # Get the bucket info for this input value for classification.
      bucketIdx = scalarEncoder.getBucketIndices(nonce)[0]

      # Run classifier to translate active cells back to scalar value.
      classifierResult = classifier.compute(
        recordNum=count,
        patternNZ=activeColumnIndices,
        classification={
          "bucketIdx": bucketIdx,
          "actValue": nonce
        },
        learn=True,
        infer=True,
      )
      #print classifierResult
      # Print the best prediction for 1 step out.
      
      oneStepConfidence, oneStep = sorted(
        zip(classifierResult[1], classifierResult["actualValues"]),
        reverse=True
      )[0]
      #print("{:16} ,{:4.4}%".format(int(oneStep), oneStepConfidence * 100))
      print(str(int(oneStep))+","+str(int(oneStepConfidence * 100)))
      #results.append([oneStep, oneStepConfidence * 100, None, None])
      
    with open("tmpsp.pkl", "w") as f:
      pickle.dump(sp, f)
    #return results


if __name__ == "__main__":
  runHotgym(_NUM_RECORDS)