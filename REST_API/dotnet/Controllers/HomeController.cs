using Microsoft.AspNetCore.Mvc;

namespace dotnet.Controllers;

[ApiController]
public class HomeController : ControllerBase
{
    [HttpGet]
    [Route("simple_read")]
    public async Task<string> Get()
    {
       return "{ message: \"x\" }";
    }

    [HttpPost]
    [Route("simple_write")]
    public async Task<string> Post(BaseItem request)
    {
        if (request.name == "x")
        {
            return "{ message: \"y\" }";
        }
        return "{ message: \"n\" }";
    }
}



//@app.get("/simple_read_sync")
//def simple_read_sync():
//    return { "message": "x"}


//@app.post("/simple_write_sync")
//def simple_write_sync(request: BaseItem):
//    try:
//        assert request.name == 'x'
//    except AssertionError:
//        return { "message": "n"}
//return { "message": "y"}
