import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model.{ContentTypes, HttpEntity}
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.unmarshalling.{FromEntityUnmarshaller, Unmarshaller}
import akka.stream.ActorMaterializer

import scala.concurrent.Future
import scala.util.{Failure, Success}

import scala.io.StdIn

import spray.json.DefaultJsonProtocol._
import spray.json._

case class SimpleData(name: String)

object Main extends App {
  implicit val system = ActorSystem("my-system")
  implicit val materializer = ActorMaterializer()
  implicit val executionContext = system.dispatcher

  implicit val simpleDataFormat = jsonFormat1(SimpleData)

  implicit val simpleDataUnmarshaller: FromEntityUnmarshaller[SimpleData] =
    Unmarshaller.byteStringUnmarshaller
      .mapWithCharset { (data, charset) =>
        val string = data.decodeString(charset.nioCharset.name)
        string.parseJson.convertTo[SimpleData]
      }

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
    path("simple_read_sync") {
      get {
        complete(HttpEntity(ContentTypes.`application/json`, """{"message": "x"}"""))
      }
    } ~
    path("simple_write_sync") {
      post {
        entity(as[SimpleData]) { data =>
          if (data.name == "x") {
            complete(HttpEntity(ContentTypes.`application/json`, """{"message": "y"}"""))
          } else {
            complete(HttpEntity(ContentTypes.`application/json`, """{"message": "n"}"""))
          }
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
