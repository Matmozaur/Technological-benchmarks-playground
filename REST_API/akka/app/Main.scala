import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model.{ContentTypes, HttpEntity}
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.unmarshalling.{FromEntityUnmarshaller, Unmarshaller}
import akka.http.scaladsl.marshalling.{ToResponseMarshaller, Marshaller, PredefinedToResponseMarshallers}
import akka.stream.ActorMaterializer

import scala.concurrent.Future
import scala.util.{Failure, Success}

import scala.io.StdIn

import spray.json.DefaultJsonProtocol._
import spray.json._

case class SimpleData(name: String)

case class CustomData(text: String, sub_text: String)

object Main extends App {
  implicit val system = ActorSystem("my-system")
  implicit val materializer = ActorMaterializer()
  implicit val executionContext = system.dispatcher

  implicit val simpleDataFormat = jsonFormat1(SimpleData)
  implicit val customDataFormat = jsonFormat2(CustomData)

  implicit val simpleDataUnmarshaller: FromEntityUnmarshaller[SimpleData] =
    Unmarshaller.byteStringUnmarshaller
      .mapWithCharset { (data, charset) =>
        val string = data.decodeString(charset.nioCharset.name)
        string.parseJson.convertTo[SimpleData]
      }

  implicit val customDataUnmarshaller: FromEntityUnmarshaller[CustomData] =
    Unmarshaller.stringUnmarshaller
      .map(data => data.parseJson.convertTo[CustomData])

  def mapToString(map: Map[String, List[Int]]): String = {
      val entries = map.map { case (key, list) =>
        s"$key -> [${list.mkString(", ")}]"
      }
      entries.mkString("\n")
    }

  def customReadF: String = mapToString(Map("message" -> (0 until 100).filter(_ % 5 == 0).toList))

  def customWriteF(request: CustomData): String =
    if (request.text.contains(request.sub_text)) """{"message": "y"}""" else """{"message": "n"}"""

  val routes =
    path("simple_read") {
      get {
        complete(HttpEntity(ContentTypes.`application/json`, """{"message": "x"}"""))
      }
    } ~
    path("simple_write") {
      post {
        entity(as[SimpleData]) { data =>
          if (data.name == "x") {
            complete(HttpEntity(ContentTypes.`application/json`, """{"message": "y"}"""))
          } else {
            complete(HttpEntity(ContentTypes.`application/json`, """{"message": "n"}"""))
          }
        }
      }
    } ~
    path("custom_read") {
      get {
         complete(HttpEntity(ContentTypes.`application/json`, customReadF))
      }
    } ~
    path("custom_write") {
        post {
          entity(as[CustomData]) { data =>
            complete(HttpEntity(ContentTypes.`application/json`, customWriteF(data)))
          }
        }
      }

  val bindingFuture = Http().bindAndHandle(routes, "0.0.0.0", 8085)

  println("Server online. Press RETURN to stop...")
  StdIn.readLine()

  // Keep the server running by waiting for a termination signal
  sys.addShutdownHook {
    bindingFuture
      .flatMap(_.unbind())
      .onComplete(_ => system.terminate())
  }
}
