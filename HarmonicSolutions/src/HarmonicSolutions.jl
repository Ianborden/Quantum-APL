module HarmonicSolutions

    using LinearAlgebra
    using JuMP
    using DifferentialEquations
    using Plots

    export HarmonicChecker
    export state_matrix
    export input_vector
    export control
    export harmonic_oscillator!
    export step!
    export integrate
    export exact_undamped
    export energy
    export Plot_helper
    export Plotter
    
    export circle_case
    export shifted_case
    export damped_case
    export beating_case
    export resonance_case
    export unbounded_resonance_case
    
    export SimpleHarmonicOscillator
    export AbstractODESolver
    export ForwardEuler
    export RungeKutta4
    export BackwardEuler
    export SymplecticEuler
    export MyODEProblem
    export ODESolution

    struct SimpleHarmonicOscillator
        m::Float64
        c::Float64
        k::Float64
        F::Float64
        w::Float64
    end

    abstract type AbstractODESolver end
    struct ForwardEuler <: AbstractODESolver end
    struct RungeKutta4 <: AbstractODESolver end
    struct BackwardEuler <: AbstractODESolver end
    struct SymplecticEuler <: AbstractODESolver end


    struct MyODEProblem{F,U,TS,P}
        f!::F
        u0::U
        tspan::TS
        p::P
    end

    struct ODESolution{T,U}
        t::T
        u::U
    end

    function HarmonicChecker(oscillator::SimpleHarmonicOscillator)
        if oscillator.m > 0 && oscillator.c >= 0 && oscillator.k >= 0
            return oscillator
        else
            return "Invalid"
        end
    end

    function state_matrix(p::SimpleHarmonicOscillator)
    A = [0 1; -1*(p.k/p.m) -1*(p.c/p.m)]
    return A
    end

    function input_vector(p::SimpleHarmonicOscillator)
        B = [0; (p.F/p.m)]
    end

    function control(t, p::SimpleHarmonicOscillator)
        u = cos(t*p.w)
        return u
    end

    function harmonic_oscillator!(dx, x, p, t)
        A = state_matrix(p)
        B = input_vector(p)
        U =  control(t, p)
        dx .= A * x + B * U
    return nothing
    end


    function step!(::ForwardEuler,f!, xnext, x, p, t, dt)
    dx = similar(x)
    f!(dx, x, p, t)
    xnext .= x + dt.* dx
    return xnext
    end

    function integrate(problem::MyODEProblem, solver::AbstractODESolver; dt)
        t0, tf = problem.tspan
        @assert tf > t0
        @assert dt > 0
        nsteps = Int(ceil((tf-t0)/dt))
        times = range(t0, tf, length = nsteps + 1)
        states = [
            similar(problem.u0)
            for _ in eachindex(times)
        ]
        states[1] .= problem.u0
        for n in 1:nsteps
            step!(solver, problem.f!, states[n+1], states[n], problem.p, times[n], dt)
        end
        return ODESolution(times, states)
    end


    function exact_undamped(ts, x0, p)
    q0, v0 = x0
    ω0 = sqrt(p.k/p.m) 
    q = q0 .* cos.(ω0 .* ts) .+ (v0 / ω0) .* sin.(ω0 .* ts)
    v = -q0 * ω0 .* sin.(ω0 .* ts) .+ v0 .* cos.(ω0 .* ts)
    return [q'; v']
    end

    function energy(x, p::SimpleHarmonicOscillator)
        q, v = x
        E = 0.5 * (p.m .* x[2]^2 + p.k .* x[1]^2)
        return E
    end

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    function step!(::RungeKutta4, f!, xnext, x, p, t, dt)
        k1 = similar(x)
        k2 = similar(x)
        k3 = similar(x)
        k4 = similar(x)
        temporary = similar(x)

        f!(k1, x, p, t)
        x2 = x + dt * k1 * 1/2
        f!(k2, x2, p, t + dt/2)
        x3 = x + dt * k2 * 1/2
        f!(k3, x3, p, t + dt/2)
        x4 = x + dt * k3
        f!(k4, x4, p, t + dt)

        xnext .= x + dt/6 * (k1 + 2k2 + 2k3 + k4)
        return xnext
    end


    function step!(::BackwardEuler, f!, xnext, x, p::SimpleHarmonicOscillator, t, dt)
        A = state_matrix(p)
        B = input_vector(p)
        n = size(A,1)
        L = Matrix(I, n, n) - dt * A
        R = x + dt * B * control(t + dt, p)

        xnext .= L \ R
        return xnext
    end


    function step!(::SymplecticEuler, f!, xnext, x, p::SimpleHarmonicOscillator, t, dt)
        q, v = x
        dx = similar(x)
        f!(dx, x, p, t)
        a = dx[2] 
        v1 = x[2] + dt * a
        q1 = x[1] + dt * v1
        
        xnext[1] = q1
        xnext[2] = v1
    return xnext
    end


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    function Plot_helper(solution)
        Q_lst = []
        V_lst = []
        for i in range(1, length(solution.u))
            append!(Q_lst,solution.u[i][1])
        end
        for i in range(1, length(solution.u))
            append!(V_lst,solution.u[i][2])
        end
        return [Q_lst, V_lst]
    end


    function Plotter(case::NamedTuple)
        problem = MyODEProblem(harmonic_oscillator!, case.u0, case.tspan, case.p)

        euler_sol = integrate(problem, ForwardEuler(); dt = case.dt)
        rk4_solution = integrate(problem, RungeKutta4(); dt = case.dt)
        symplectic_solution = integrate(problem, SymplecticEuler(); dt = case.dt) 
        backward_euler = integrate(problem, BackwardEuler(), dt = case.dt)

        Exact = exact_undamped(euler_sol.t, case.u0, case.p)
        Exact_lst_q = []
        Exact_lst_v = []
        for i in range(1, length(Exact))
            if iseven(i)
                append!(Exact_lst_q, Exact[i])
            else
                append!(Exact_lst_v, Exact[i])
            end
        end
        Plots.plot()
        Plots.plot!(euler_sol.t,Plot_helper(euler_sol)[1], label = "Forward", color=:red, size = (1200,600))
        Plots.plot!(euler_sol.t,Plot_helper(backward_euler)[1], label = "Backward", title =  case.name, color=:blue)
        Plots.plot!(euler_sol.t,Plot_helper(symplectic_solution)[1], label = "Symplectic", color=:orange)
        Plots.plot!(euler_sol.t,Plot_helper(rk4_solution)[1], label = "RK4", color=:green)
        Plots.plot!(euler_sol.t,Exact_lst_q, label = "Exact", color=:black, line =:dash)
    end


    circle_case = (name = "undamped unit circle",
    p = SimpleHarmonicOscillator(1.0,0.0,1.0,0.0,0.0,),
    u0 = [1.0, 0.0],tspan = (0.0, 20π),dt = 0.05)

    shifted_case = (name = "constant force and shifted equilibrium", 
    p = SimpleHarmonicOscillator(1.0, 0.0, 1.0, 1.0, 0.0,),
    u0 = [0.0, 0.0], tspan = (0.0, 10π), dt = 0.05)

    damped_case = (name = "damped inward spiral",
    p = SimpleHarmonicOscillator(1.0,0.2,1.0,0.0,0.0,),
    u0 = [1.0, 0.0], tspan = (0.0, 30.0),dt = 0.05)

    beating_case = (
    name = "near-resonant beating",
    p = SimpleHarmonicOscillator(1.0,0.0,1.0,0.15,0.9,),
    u0 = [0.0, 0.0],tspan = (0.0, 150.0),dt = 0.02,)

    resonance_case = (
    name = "damped resonant forcing",
    p = SimpleHarmonicOscillator(1.0,0.15,1.0,0.15,1.0,),
    u0 = [0.0, 0.0],tspan = (0.0, 100.0),dt = 0.02,)

    unbounded_resonance_case = (
    name = "undamped exact resonance",
    p = SimpleHarmonicOscillator(1.0,0.0,1.0,0.03,1.0,),
    u0 = [0.0, 0.0],tspan = (0.0, 100.0),dt = 0.02,)

end # module HarmonicSolutions