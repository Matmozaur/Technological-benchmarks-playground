import org.slf4j.LoggerFactory
import akka.http.scaladsl.Http
import akka.http.scaladsl.model.{ContentTypes, HttpEntity}
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.server.Route
import akka.actor.ActorSystem
import scala.concurrent.Future
import scala.io.StdIn

case class BaseItem(name: String)

object Main extends App {
val log = LoggerFactory.getLogger(getClass)

implicit val system = ActorSystem("my-system")
implicit val executionContext = system.dispatcher

val route: Route =
concat(
path("simple_read") {
get {
complete(HttpEntity(ContentTypes.application/json, "{"message": "x"}"))
}
},
path("simple_write") {
post {
entity(as[BaseItem]) { request =>
if (request.name == "x") {
complete(HttpEntity(ContentTypes.application/json, "{"message": "y"}"))
} else {
complete(HttpEntity(ContentTypes.application/json, "{"message": "n"}"))
}
}
}
},
path("simple_read_sync") {
get {
complete(HttpEntity(ContentTypes.application/json, "{"message": "x"}"))
}
},
path("simple_write_sync") {
post {
entity(as[BaseItem]) { request =>
if (request.name == "x") {
complete(HttpEntity(ContentTypes.application/json, "{"message": "y"}"))
} else {
complete(HttpEntity(ContentTypes.application/json, "{"message": "n"}"))
}
}
}
}
)

val bindingFuture = Http().newServerAt("localhost", 8080).bind(route)

log.info("Server online at http://localhost:8080/\nPress RETURN to stop...")
StdIn.readLine()

bindingFuture
.flatMap(.unbind())
.onComplete( => system.terminate())
}