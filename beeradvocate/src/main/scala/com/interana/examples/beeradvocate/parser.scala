package com.interana.examples.beeradvocate

import scala.io.Source
import java.io._
import java.util.zip.GZIPInputStream

object parser extends App {

  val beerReviewPath = "data/beeradvocate"
  val beerReviewSuffix = ".txt.gz"

  def makeInputStream(i: Int) = {
    val f = beerReviewPath + i.toString() + beerReviewSuffix
    System.err.println("Opening " + f)
    new GZIPInputStream(
      new BufferedInputStream(
        new FileInputStream(f)))
  }

  // functional programming FTW!
  val beerReviewStream = (3 until 6).foldLeft(
    new SequenceInputStream(makeInputStream(1), makeInputStream(2)))(
    (s:InputStream, i:Int) => new SequenceInputStream(s, makeInputStream(i)))

  val beerReviewSource = Source.fromInputStream(beerReviewStream)

  var buffer = new StringBuilder()

  val BeerName = "beer/name:\\s(.+)".r
  val BeerId = "beer/beerId:\\s(\\d+)".r
  val BrewerId = "beer/brewerId:\\s(\\d+)".r
  val ABV = "beer/ABV:\\s([\\.\\d]+)".r
  val BeerStyle = "beer/style:\\s(.*)".r
  val ReviewAppearance = "review/appearance:\\s(.*)".r
  val ReviewAroma = "review/aroma:\\s([\\.\\d]+)".r
  val ReviewPalate = "review/palate:\\s([\\.\\d]+)".r
  val ReviewTaste = "review/taste:\\s([\\.\\d]+)".r
  val ReviewOverall = "review/overall:\\s([\\.\\d]+)".r
  val ReviewTime = "review/time:\\s(\\d+)".r
  val ReviewProfileName = "review/profileName:\\s(.*)".r
  val ReviewText = "review/text:\\s(.*)".r
  val Empty = "^$".r

  var beerName:String = null
  var beerId:Int = 0
  var brewerId:Int = 0
  var aBV:Float = 0.0f
  var beerStyle:String = null
  var reviewAppearance:Float = 0.0f
  var reviewAroma:Float = 0.0f
  var reviewPalate:Float = 0.0f
  var reviewTaste:Float = 0.0f
  var reviewOverall:Float = 0.0f
  var reviewTime:Long = 0L
  var reviewProfileName:String = null
  var reviewText:String = null

  val out = new PrintWriter("beerReviews.json")
  for (line <- beerReviewSource.getLines()) {

    line match {
      case BeerName(x) => beerName = x
      case BeerId(x) => beerId = x.toInt
      case BrewerId(x) => brewerId = x.toInt
      case ABV(x) => aBV = x.toFloat * 100
      case BeerStyle(x) => beerStyle = x
      case ReviewAppearance(x) => reviewAppearance = x.toFloat * 100
      case ReviewAroma(x) => reviewAroma = x.toFloat * 100
      case ReviewPalate(x) => reviewPalate = x.toFloat * 100
      case ReviewTaste(x) => reviewTaste = x.toFloat * 100
      case ReviewOverall(x) => reviewOverall = x.toFloat * 100
      case ReviewTime(x) => reviewTime = x.toLong
      case ReviewProfileName(x) => reviewProfileName = x
      case ReviewText(x) => reviewText = x
      case "" => {
        val r = new review(beerName, beerId, brewerId,
          aBV, beerStyle,
          reviewAppearance, reviewAroma, reviewPalate,
          reviewTaste, reviewOverall, reviewTime, reviewProfileName,
          reviewText)
        out.println(r.mkString)
        // reset
        beerName = null
        beerId = 0
        brewerId = 0
        aBV = 0.0f
        beerStyle = null
        reviewAppearance = 0.0f
        reviewAroma = 0.0f
        reviewPalate = 0.0f
        reviewTaste = 0.0f
        reviewOverall = 0.0f
        reviewTime = 0L
        reviewProfileName = null
        reviewText = null
      }
      case _ => Unit

    }
  }

  beerReviewSource.close()
  out.close()

}
