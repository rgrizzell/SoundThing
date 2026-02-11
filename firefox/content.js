function docReady(fn) {
  // see if DOM is already available
  if (
    document.readyState === "complete" ||
    document.readyState === "interactive"
  ) {
    // call on next available tick
    setTimeout(fn, 1000);
  } else {
    document.addEventListener("DOMContentLoaded", fn);
  }
}

docReady(function () {
  watchPlayCtrl();
  watchSoundbadge();
  //watchTime();
  SendPlayCtrl();
});

var SendMetadata;
var SendPlayCtrl;
//var SendTime;

function watchSoundbadge() {
  let soundbadge = document.getElementsByClassName(
    "playControls__soundBadge",
  )[0];

  SendMetadata = (_) => {
    // send new song data
    let artist = soundbadge.getElementsByClassName(
      "playbackSoundBadge__lightLink",
    )[0].title;
    let title = soundbadge.getElementsByClassName(
      "playbackSoundBadge__titleLink",
    )[0].title;
    let icon_span = soundbadge.querySelector("span.sc-artwork");
    let icon_url = icon_span.style.backgroundImage
      .slice(4, -1)
      .replace(/"/g, "");
    //let time_data = getTimeData();
    //let song_href = soundbadge.querySelector("a.playbackSoundBadge__avatar").getAttribute("href");

    // let metadata = {
    //     artist: artist,
    //     song: song,
    //     icon_url: icon_url,
    //     // time: time_data.time + "000000",
    //     // length: time_data.length + "000000",
    //     song_href: song_href,
    // };

    sendTrackInfo(artist, title, icon_url);
  };

  observer = new MutationObserver(SendMetadata);

  let config = {
    /*attributes: true, characterData: true,*/ subtree: true,
    childList: true,
  };
  observer.observe(soundbadge, config);
}

function watchPlayCtrl() {
  let target = document.getElementsByClassName("playControl")[0];

  SendPlayCtrl = (_) => {
    if (target.classList.contains("playing")) {
      console.log("Playing");
    } else {
      console.log("Paused");
    }

    //SendMetadata();
  };

  let observer = new MutationObserver(SendPlayCtrl);
  let config = {
    attributes: true,
    childList: true,
    characterData: true,
    subtree: true,
  };
  observer.observe(target, config);
}

// function watchTime() {
//     let timeline = document.getElementsByClassName("playControls__timeline")[0];

//     let observer = new MutationObserver((_) => {
//         let timeData = getTimeData();
//         // TODO: decide on if this is necessary
//     });
//     let config = { attributes: true, childList: true, characterData: true, subtree: true };
//     observer.observe(timeline, config);
// }

// function getTimeData() {
//     let timeline = document.getElementsByClassName("playControls__timeline")[0];
//     let progressBar = timeline.querySelector(".playbackTimeline__progressWrapper[role='progressbar']");
//     let time = progressBar.getAttribute("aria-valuenow");
//     let length = progressBar.getAttribute("aria-valuemax");
//     return {
//         time: time,
//         length: length,
//     };
// }

// let bgPort = browser.runtime.connect({name: "contentPort"});
// bgPort.onMessage.addListener((m) => {
//     switch (m.type) {
//         case "playpause":
//             document.querySelector('.playControl').click();
//             break;
//         case "prev":
//             document.querySelector('.skipControl__previous').click();
//             break;
//         case "next":
//             document.querySelector('.skipControl__next').click();
//             break;
//         case "raise":
//             window.focus();
//         default:
//             console.log("unknown format", m);
//             break;
//     }
// });

// function sendMessage(type, data) {
//     if (bgPort.error) {
//         console.log(bgPort.error)
//     } else {
//         bgPort.postMessage({
//             type: type,
//             data: data,
//         })
//     }
// }

async function sendTrackInfo(artist, title, image) {
  var metadata = JSON.stringify({
    artist: artist,
    title: title,
    image: image,
  });
  console.log("Sending track info: " + metadata);

  // var xhr = new XMLHttpRequest();
  // xhr.open("POST", "http://192.168.200.163:5000/track-info");
  // xhr.setRequestHeader("Content-Type", "application/json");

  // // Handle the response from the server.
  // xhr.onreadystatechange = function () {
  //   if (xhr.readyState === 4 && xhr.status === 200) {
  //     console.log("Track info sent successfully.");
  //   }
  // };

  // Handle any errors that occur during the request.
  // xhr.onerror = function () {
  //   console.log("Error sending track info: " + xhr.statusText);
  // };

  const url = "http://192.168.200.163:5000/track-info";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: metadata,
  };

  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.text();
    console.log(result);
  } catch (error) {
    console.error(error.message);
  }
}
