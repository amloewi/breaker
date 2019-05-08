# Breaker: An Emergency Mindfulness Minigame

Breaker is a small piece of software with a large ambition: to get you back on track when you're wasting time. It accomplishes this through a very elegant design ... and a very inelegant codebase.

## The Game

When you realize you're wasting time, either staring at your screen blankly, or flipping constantly through tabs without actually reading any of them -- but for some reason *just can't stop* -- instead of the hotkey for a new tab, just hit the hotkey for Breaker, and you enter -- **The Game**.

No matter what application is running, you're suddenly presented with a black screen, and the words "Breathe in...". Press any key to continue, and you'll see a moving sine wave, with a stationary vertical line. This is **The Game**. To play, there are three rules:

- When the line is on the **UPWARDS** part of the wave, press **NOTHING**
- When the line is on the **DOWNWARDS** part of the wave, press **SPACE**
- **BREATHE**: *IN* on the *UP* part, *OUT* on the *DOWN* part. Like the wave.

And that's it!

If you don't do this well enough -- meaning, press space too much when the wave is moving up, or *don't* press space enough when the wave is moving down -- then you'll need to try again. The game exits either when you follow the wave closely enough, or automatically after three tries.

## Hotkeys and Setup

The easiest way to get Breaker to work right now is to set it up as a Service using Automator (on Mac -- I have no idea how Windows or Linux work). That way you can bind a system-level hotkey to it, and get the game to play by running the Automator workflow. If you don't know how to do that you can look up instructions online (like I did), but here are the basic steps.

- With the Mac application Automator, create a new Service
- Have the service Run a Bash Script
- The script should run with NO input
- The contents of that script should look something like
  ```
  python ~/Documents/breaker/waves.py
  ```
  or more generally,
  ```
  your-desired-version-of-python the-path-to-breaker/waves.py
  ```
  And be forewarned, the Automator python may be different from the system one! Don't be afraid to specify the full path to your desired python e.g.
  ```
  /Users/username/anaconda3/bin/python ~/Code/breaker/waves.py
  ```
  if you're having trouble.
- RESTART YOUR COMPUTER: The Service may only be registered after you've done this (and it's infuriating until then!).
- Set your desired key combination trigger in Finder > Services > Services Preferences. I've found that Shift-Command-Y is an easy key combo that won't conflict with too many other combinations (which can be a serious problem, and may be the reason your chosen combination isn't working).

## Dependencies

Breaker requires `pygame` to run, but no other libraries that don't come automatically as part of python. It implements its own correlation function in order to avoid a `numpy` dependency.


## Making Actual Software

It would obviously be so much better if it wasn't necessary to use Automator, but I don't know how to do Cocoa/Mac development, and haven't been able to package the current code using `pyinstaller` etc. The next major step for this project is to figure out how to turn it into a normal Mac app that could run in the menu bar, and be easily and self-containedly installed by people who don't know how to code. If you'd like to push things in that direction, let's talk!


## The Philosophy

Breaker is a simple project with a lot of thoughts behind it. This is the reasoning behind the design, and how it compares to the other popular software approaches to this problem.

When you're distracted, you're in a pretty deep catch-22. You need to get out of that headspace, but you also need headspace to *get* you out of that headspace. Of course this isn't a new problem, but all the solutions I know of have some pretty serious problems. They fall pretty neatly into three buckets.

### Blockers are Too Rigid *And* Too Weak

The first, simplest, and probably most widely used approach, is a blocker of some kind. There are many, and they have many subtle differences, but the idea is always the same -- keeping you from accessing particular programs, particular websites, or even the internet altogether.

The biggest problem with blockers for me is that I have *always* found ways around them, and usually within minutes of installing a new one. I may be pushed to do this because I'm still in a time-wasting mindset -- the blockers don't even try to change that -- or because I actually need the website I just locked myself out of! Either way, they don't do what I want them to.


### Meditation Apps *Require* Effort

Meditation is popular because meditation is powerful. But meditation is powerful because meditation is *hard*. And all of the apps that I've seen that claim they'll get you back on track require effort to open, start, and use. If you were focussed enough to go sit in a quiet place and watch your breath -- or even focussed enough to *close the website you can't stop scrolling through* -- you wouldn't have a problem! In other words, tons of these apps simply miss the point. When you only have a tiny amount of self-control left, you need an emergency switch that only *requires* a tiny amount of self-control.


### Automatic Timers Don't *Demand* Effort (and are Obnoxious)

The last major approach to the get-you-focussed-again problem is programs that have automatic timers. These are apps that automatically lock you out of your computer, or flash messages asking you to stand up and walk around. Having these trigger every X minutes certainly solves the problem of barrier to entry, by removing it entirely, and don't have the heavy-handedness of blockers. However, they reveal two other serious issues.

The first is that if you're on a distracted tear, then you have a certain amount of mental inertia. If your computer isn't working all of a sudden, you can quickly shift your mind onto something else, check your phone for thirty seconds while the countdown runs, go to the bathroom, come back, and keep doing exactly what you were doing. Your body was stopped, but your mind was untouched.

And if that wasn't enough, I find automated timers to be just awful! I *hate* having alarms go off, or things pop up, or my screen be grayed out, when I'm in the middle of something -- and since your computer can't tell when you're distracted and when you aren't, you're going to be inevitably bothered during productive times as well. (Your computer can't tell easily, in any event -- that would be a much more sophisticated if not impossible program.)

### So What do you Need?

You need something that:
- Gives you access to what you need, but also
- Lets you choose to restrict yourself
- In a way that is precise
- Dynamic
- Extremely low-effort
- *And effective.* It needs to solve not just the symptom (access) but the problem itself (your state of mind).

Here's how Breaker solves all of these problems.


### Breaker: Easy to Start, Hard to Ignore, Controlled by You

Let's start with the real problem, and work from there -- your state of mind. Meditation has a lot to add here, but it's a little too heavy as a whole, so let's strip it down to the mechanical basics -- breathing, and focus.

Taking a slow, deep, breath has immediate physiological effects. It slows your heart-rate, and generally activates your parasympathetic nervous system (the slower calmer parts). This makes it easier for your mind to settle, but it still needs a pull, to go with the push.

This pull is in the game. It asks you not just to breathe, but to breathe while paying close attention to a simple, distraction-free prompt, actively clearing your mind of whatever was driving you to just keep opening more tabs.

And last, but perhaps most importantly, it *requires* you to do this! Or at least, gets as close as a computer can get, without strapping a gas meter to you. The in-out-up-down connection between breathing, and button-pressing, allows the software to demand that you perform a breathing-like activity, and by having a long sine-wave, actually demand that you perform a *deep* breathing-like activity, unlike the automatic popups, that will go away no matter what. (It obviously can't actually tell if you're breathing, but if you're going to be pressing the button in a slow cyclical pattern anyway, it would be pretty perverse to refuse to breathe along with it.) It's this interactive connection between the actually-useful exercise (deep/slow breathing) and the gatekeeping device itself (the computer) that gives Breaker its real power as a behavior enforcer.

In summary,

- The game comes up only, and exactly, when you want it to
- Triggering the game requires only a split-second's thought and near-zero effort
- It holds your hand through a fast, easy, and painless exercise with verifiable physiological and psychological effects
- It actually *requires* you to go through the exercise, instead of just *hoping* you will.

If you find this exciting, or have ideas about how to make it even better, don't hesitate to get in touch or fork the repo!
