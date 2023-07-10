import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model.{ContentTypes, HttpEntity}
import akka.http.scaladsl.server.Directives._
import akka.stream.ActorMaterializer
import scala.io.StdIn

object Main extends App {
  implicit val system = ActorSystem("my-system")
  implicit val materializer = ActorMaterializer()
  implicit val executionContext = system.dispatcher

  val routes =
    path("simple_read") {
      get {
        complete(HttpEntity(ContentTypes.`application/json`, """{"message": "x"}"""))
      }
    } ~
    path("simple_write") {
      post {
        entity(as[Map[String, String]]) { data =>
          if (data.get("name").contains("x")) {
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
        entity(as[Map[String, String]]) { data =>
          if (data.get("name").contains("x")) {
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

  bindingFuture
    .flatMap(_.unbind())
    .onComplete(_ => system.terminate())
}
