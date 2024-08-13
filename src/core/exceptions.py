import copy

from typing import Any

from fastapi import HTTPException


class BaseHTTPException(HTTPException):

    exc_message = {
        400: "Ошибка запроса",
        401: "Ошибка аутентификации",
        404: "Объект не найден",
        422: "Ошибка валидации входных данных",
        403: "Недостаточно прав",
    }

    def __init__(
        self,
        status_code: int,
        msg: str = None,
        extra: str = "",
        detail: Any = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.status_code = status_code
        self.extra = extra
        self.msg = msg

    def _response_error(self, exception_: dict) -> dict:
        try:
            return self._modify_exception(exception_)
        except (IndexError, KeyError, AttributeError):
            return exception_

    @staticmethod
    def _modify_exception(exception_: dict) -> dict:
        if not all([exception_.get("detail"), exception_.get("body")]):
            return exception_
        response_detail = []
        target_locs = [loc["loc"][-1] for loc in exception_["detail"] if loc.get("loc")]
        path = None
        for detail in exception_["detail"]:
            tmp_exception = copy.deepcopy(exception_)
            if not detail.get("loc"):
                continue
            for index, loc in enumerate(detail["loc"]):
                if not path:
                    path = tmp_exception[loc]
                    continue
                if index == len(detail["loc"]) - 1:
                    path[loc] = detail["msg"]
                    tmp_path = copy.deepcopy(path)
                    for k in tmp_path:
                        if k not in target_locs:
                            del path[k]
                        else:
                            del target_locs[target_locs.index(k)]
                    path = None
                    continue
                path = path[loc]
            response_detail.append({"body": tmp_exception["body"]})
        exception_["error_list"] = response_detail
        return exception_

    def get_response(self, pydantic_exception: dict = None):
        if not pydantic_exception:
            if self.status_code not in self.exc_message:
                raise KeyError(f"Статус код <{self.status_code}> не найден")
            return {
                "msg": (
                    self.exc_message.get(self.status_code) if not self.msg else self.msg
                ),
                "extra": {"detail": self.extra},
            }
        return {
            "msg": "Ошибка валидации входных данных",
            "extra": {**self._response_error(pydantic_exception)},
        }


def exception(
    status_code: int,
    msg: str = None,
    extra: str = "",
) -> BaseHTTPException:
    return BaseHTTPException(status_code=status_code, msg=msg, extra=extra)
