import asyncio, time, json
from kasa import SmartStrip

def turnon(light, st="shelfstrip.lan"):
    try:
        strip = SmartStrip(st)
        asyncio.run(strip.update())
        asyncio.run(strip.children[light].turn_on())
    except:
        print("error: turnon strip fail")

def turnoff(light, st="shelfstrip.lan"):
    try:
        strip = SmartStrip(st)
        asyncio.run(strip.update())
        asyncio.run(strip.children[light].turn_off())
    except:
        print("error: turnoff strip fail")

def state(st="shelfstrip.lan"):
    try:
        strip = SmartStrip(st)
        asyncio.run(strip.update())
        state = ""
        for i in range(0,3):
            state = state + str(strip.children[i].is_on)

        return state
    except:
        print("error: turnoff strip fail")
        return "fff"
    

if __name__ == "__main__":
    st="shelfstrip.lan"
    strip = SmartStrip(st)
    asyncio.run(strip.update())

    print(json.dumps(state()))


