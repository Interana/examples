package com.interana.examples.beeradvocate

import scala.util.parsing.json.JSONObject

/**
 * Created by jadler on 5/2/14.
 */
class review(_name:String, _beerId:Int, _brewerId:Int, _abv:Float,
              _style: String, _appearance: Float,
              _aroma: Float, _palate: Float,
              _taste: Float, _overall: Float,
              _time: Long, _profileName: String,
              _text: String) {
  val name = _name
  val beerId = _beerId
  val brewerId = _brewerId
  val ABV = _abv
  val style = _style
  val appearance = _appearance
  val aroma = _aroma
  val palate = _palate
  val taste = _taste
  val overall = _overall
  val time = _time
  val profileName = _profileName
  val text = _text

  def asMap = {
    Map(
      "name" -> name, "beerId" -> beerId,
      "brewerId" -> brewerId, "ABV" -> ABV,
      "style" -> style, "appearance" -> appearance, "aroma" -> aroma,
      "palate" -> palate, "taste" -> taste, "overall" -> overall,
      "time" -> time, "profileName" -> profileName, "text" -> text
    )
  }

  def mkString = {
    val jsonObject = new JSONObject(this.asMap)
    jsonObject.toString()
  }

}
