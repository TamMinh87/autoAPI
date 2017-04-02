from libs.core.core.service_utils import send_request

from config.config_reader import config_common as config


def _send_to_url(url, method='GET', json=None, params=None, header=None):
    if not header:
        header = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijc3ZDcwYmYxMDFmOWZiZWE0NjY5O'
                             'DhkYWYwMTE2YWE1MTkzZTgyZDAyYjQzZDE1ZTg2YTdiOGM4MjNmZmM5NTEwMDc2NzQ4OGRiMzBmODNj'
                             'In0.eyJhdWQiOiIyIiwianRpIjoiNzdkNzBiZjEwMWY5ZmJlYTQ2Njk4OGRhZjAxMTZhYTUxOTNlODJkMDJ'
                             'iNDNkMTVlODZhN2I4YzgyM2ZmYzk1MTAwNzY3NDg4ZGIzMGY4M2MiLCJpYXQiOjE0OTEwMTk0OTQsIm5iZi'
                             'I6MTQ5MTAxOTQ5NCwiZXhwIjoxNDkyMzE1NDk0LCJzdWIiOiIzMiIsInNjb3BlcyI6WyIqIl19.mMy7zfdw'
                             '0bR2BZnh3ciHFCKYiebQZzFi8GR_CPt_1AJ4tKkBXK3UVqo_Llbx1We1sI91L8rH4OKfPWmZxlKEdUiHFct'
                             'xTHZZMHEoK4PgrHtCLLt2YktI2jcYkLZ38NL_77Do5jEnRZSIPt_aQ_IpaLELxPBoGpiJEwmx9yYgAw9vsG'
                             'xypgbUiydNP52IkAAoak0D3JW0MFaTgat9__DRmQOijV3quT-RFIcEmqHYh9o1FHO5Uc69-fAbnyvIucbuZ'
                             'WBVQ_3iGwhx-4zqXUTSoue-ydtW-ojFUxYBRGNgCL7InDHECJlZuGl-erV43DcZZH1AYEM8GrBguID0-0oX'
                             'rjOnSiZxwwt4LJG1WwGNZohLwuwCFdB3X6UFYPTNfAqLfggf-iNdiTIGnR0tC9gOpm5Ckio7DJCP4sfzFMe'
                             '6D3W0vZKzmHzrS52ynZ_tIGGrHQ9Qd3MSWoT4Ec6X0Kjh3QjrGYWQe_MyQ-2rQcZKCzw0GAwCKYao2pbI9G'
                             'oc1TThp2RyJgRznmeyN0lkkwcfyKg-EYWt_vQkXG-8ZGL-d_GTShkiTiNKP52r00Rym1FjIRa6GdNuo3p2O'
                             'b2zx7a42Z7JEuQNSUNn-W86qlv2APIbo5A_leb-QLcI5BaoXgWTk7Hh7J-g8vZsPKQIyEu44qOZQqQnoOIE'
                             'KrK82IYoZmc'
        }
    return send_request(url=url, method=method, json=json, params=params, headers=header)


def create_rewards(json):
    return _send_to_url(config.get('reward_api', 'create_reward'), method='POST', json=json)
